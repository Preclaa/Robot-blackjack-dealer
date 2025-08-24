import random
import requests
import os
import copy
import asyncio
import json
import cv2
import numpy as np
import base64
from datetime import datetime   

from ultralytics import YOLO
from scipy.spatial.transform import Rotation as R

from fastapi import WebSocket, WebSocketDisconnect

from connection import ConnectionManagerGame, ConnectionManagerLog, ConnectionManagerWebcam
from models import Configuration, GameState, GameStatus, PlayerState, PlayerStatus, Pose, Position, Orientation, LogItem, LogSeverity

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
ARCOR2_API_URL = os.getenv("ARCOR2_API_URL", "http://192.168.104.100:5012")

class Dealer:
    def __init__(self):
        self.camera = ConnectionManagerWebcam()
        self.logger = ConnectionManagerLog()
        self.game = ConnectionManagerGame()
        
        self.camera_request = asyncio.Queue()
        self.camera_images = asyncio.Queue()
        
        self.configurations: dict[str, Configuration] = {}
        self.position_custom: dict[str, Pose] = {}
        
        # Set default values
        self.turn_cards = False
        self.simulation_mode = False 
        
        self.player_count = 3
        self.cards_in_deck = 52
        
        self.card_detector = YOLO('card_detector.pt')
        self.robot_velocity = 50
        
        self.pose = Pose(
                orientation=Orientation(w=1.0, x=0, y=0, z=0),
                position=Position(x=0, y=0, z=0)
            )

        self.game_state = GameState(
            status=GameStatus.NOT_STARTED,
            turn=0,
            players={
                i: PlayerState(status=PlayerStatus.DISCONNECTED,hand=[], score=0) for i in range(self.player_count + 1)
            }
        )

        self.load_positions()
        self.arcor2_get_current_pose()

    def load_positions(self):
        """Loads saved positions from a JSON file or creates them if they do not exist
        """
        
        self.active_configuration = "default"
        if not os.path.exists("positions.json"):
            deck = Pose(
                position=Position(x=0.0, y=0.0, z=0.0),
                orientation=Orientation(w=1.0, x=0.0, y=0.0, z=0.0)
            )

            offsets = {
                "dealer": Position(x=0.0, y=0.0, z=0.0),
                "player": Position(x=0.0, y=0.0, z=0.0),
                "player_card": Position(x=0.0, y=0.0, z=0.0),
                "next_player": Position(x=0.0, y=0.0, z=0.0),
                "card_flipper": Position(x=0.0, y=0.0, z=0.0),
            }
            

            with open("positions.json", "w") as file:
                json.dump({"default": {
                    "deck": deck.model_dump(),
                    "offsets": {k: v.model_dump() for k, v in offsets.items()}
                }}, file, indent=2)

        if os.path.exists('positions.json'):
            with open("positions.json", "r") as file:
                data = json.load(file)
                self.configurations = {k: Configuration.model_validate(v) for k, v in data.items()}
            
        if os.path.exists('positions_custom.json'):
            with open("positions_custom.json", "r") as file:
                data = json.load(file)
                self.position_custom = {k: Pose.model_validate(v) for k, v in data.items()}
        
    async def arcor2_start(self):
        """Starts the ARCOR2 API
        """
        url = f"{ARCOR2_API_URL}/state/start"
    
        data = {
            "pose": Pose(
                orientation=Orientation(w=0.92388, x=0.38268, y=0, z=0),
                position=Position(x=0, y=0, z=0)
            ).model_dump()
        }
        response = requests.put(url, json=data)
        if response.status_code == 204:
            await self.logger.log(LogItem(type=LogSeverity.INFO, message="ARCOR2 API started"))
        else:
            await self.logger.log(LogItem(type=LogSeverity.ERROR, message=f"ARCOR2 API failed to start: {response.status_code} {response.text}"))
        
    async def arcor2_stop(self):
        """Stops the ARCOR2 API
        """
        url = f"{ARCOR2_API_URL}/state/stop"

        response = requests.put(url)
        if response.status_code == 204:
            await self.logger.log(LogItem(type=LogSeverity.INFO, message="ARCOR2 API stopped"))
        else:
            await self.logger.log(LogItem(type=LogSeverity.ERROR, message=f"ARCOR2 API failed to stop: {response.status_code} {response.text}"))
        
    
    def arcor2_get_current_pose(self):
        """Sets the current value of pose
        """

        try:
            url = f"{ARCOR2_API_URL}/eef/pose"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.pose = Pose.model_validate(response.json())
        except requests.RequestException as e:
            self.simulation_mode = True
        
    def arcor2_set_pose(self, pose: Pose):
        """Sends the pose to ARCOR2 API, moves the robot

        :param pose: Destination pose for the robot
        """
        self.pose = copy.deepcopy(pose)
        
        if self.simulation_mode:
            return

        url = f"{ARCOR2_API_URL}/eef/pose?velocity={self.robot_velocity}&payload=1"
        data = pose.model_dump()

        headers = {'Content-type': 'application/json'}
        requests.put(url, json=data, headers=headers)

        
    def arcor2_start_vacuum(self):
        """Starts the vacuum suction on ARCOR2 API.
        """
        if self.simulation_mode:
            return
        
        url = f"{ARCOR2_API_URL}/suction/suck?vacuum=70"
        requests.put(url)

    def arcor2_stop_vacuum(self):
        """Stops the vacuum suction on ARCOR2 API.
        """
        if self.simulation_mode:
            return
        
        url = f"{ARCOR2_API_URL}/suction/release"
        requests.put(url)
        
    async def ws_players(self, websocket: WebSocket, position):
        """Handles the WebSocket logic for players

        :param websocket: WebSocket connection for the player
        :param position: Position of the player in the game (0 for dealer, 1-3 for players)
        """
        connected = await self.game.connect(websocket, position)
        if not connected:
            await self.logger.log(LogItem(type=LogSeverity.WARNING, message=f"Someone tried to connect to already occupied position {position}"))
            return
        elif position > 0:
            await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Player {position} connected"))    

        self.game_state.players[position].status = PlayerStatus.LOBBY_WAITING
        self.game_state.players[position].hand = []
        self.game_state.players[position].score = 0
        
        await self.game.broadcast(self.game_state.model_dump_json())
        
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Player actions
                if message.get("action") == "ready":
                    await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Player {position} READY"))
                    await self.player_ready(position)
                    
                elif message.get("action") == "stand":
                    await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Player {position} STAND"))
                    await self.stand()
                
                elif message.get("action") == "hit":
                    await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Player {position} HIT"))
                    await self.hit(position)
                    
                await self.game.broadcast(self.game_state.model_dump_json())

        except WebSocketDisconnect:
            if position in self.game.active_connections:
                del self.game.active_connections[position]
            await self.remove_player(position)
            
            await self.game.broadcast(self.game_state.model_dump_json())

    async def ws_camera(self, websocket: WebSocket):
        """Handles the WebSocket logic for the camera
        
        :param websocket: WebSocket connection for the camera
        """
        
        await self.camera.connect(websocket)
        
        await self.logger.log(LogItem(type=LogSeverity.DEBUG, message=f"Camera connected"))
        
        try:
            while True:
                # Wait for camera request
                await self.camera_request.get()
                self.camera_request.task_done()      
                
                # Ping camera
                await self.camera.send()   
                
                # Put image in queue
                data = await websocket.receive_text()
                await self.camera_images.put(data)
                            
        except WebSocketDisconnect:
            await self.camera.disconnect()
        
    async def ws_logger(self, websocket: WebSocket):
        """Handles the WebSocket logic for the logger

        :param websocket: WebSocket connection for the logger
        """
        await self.logger.connect(websocket)
        
        await self.logger.log(LogItem(type=LogSeverity.DEBUG, message=f"Logger connected"))
        
        await self.logger.log(LogItem(type=LogSeverity.DEBUG, message=f"SIMULATION: {self.simulation_mode}"))
        await self.logger.log(LogItem(type=LogSeverity.DEBUG, message=f"FLIP: {self.turn_cards}"))
        await self.logger.log(LogItem(type=LogSeverity.DEBUG, message=f"ROBOT VELOCITY: {self.robot_velocity}"))
        await self.logger.log(LogItem(type=LogSeverity.DEBUG, message=f"ACTIVE CONFIGURATION: {self.active_configuration}"))
        
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            await self.logger.disconnect()
                    
    async def remove_player(self, position):
        """Disconnects a player from the game

        :param position: _description_
        """
        self.game_state.players[position].status = PlayerStatus.DISCONNECTED
        await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Player {position} disconnected"))
        
        if self.game_state.status == GameStatus.ROUND_ENDED:
            await self.check_ready()
        elif self.game_state.status in [GameStatus.IN_PROGRESS, GameStatus.DEALING] and self.game_state.turn == position:
            await self.next_player_turn()
                    
    async def pick_card(self):
        """Picks a card from the deck without turning it over"""
        self.move_to_deck()
        self.arcor2_start_vacuum()
        self.move_to_deck(-0.2)
                    
    async def pick_card_turn(self):
        """Picks a card from the deck and turns it over
        
            Function performs series of movements to pick a card from the deck and turn it over
            Positions (offsets) were manually tested to perform consistent card flipping
        """

        self.move_to_deck()
        self.arcor2_start_vacuum()
        self.move_to_deck(-0.2)
        
        flipper_offset = self.configurations[self.active_configuration].offsets["card_flipper"]
        flipper_position = copy.deepcopy(self.configurations[self.active_configuration].deck)
        
        # Move to the flipper position
        flipper_position.position += flipper_offset + Position(x=0, y=-0.1, z=0)
        self.arcor2_set_pose(flipper_position)
        
        # Rotate robot so the angle matches the flipper
        flipper_position.orientation = self.rotate(flipper_position.orientation, "x", 50)
        flipper_position.position += Position(x=0, y=0, z=-0.1)
        self.arcor2_set_pose(flipper_position)
        
        # Lower the robot and drop the card
        flipper_position.position += Position(x=0, y=0.13, z=0)
        self.arcor2_set_pose(flipper_position)
        self.arcor2_stop_vacuum()
        
        # Move robot up
        flipper_position.position += Position(x=0, y=-0.1, z=0)
        self.arcor2_set_pose(flipper_position)
    
        # Reset to position without rotation, perform a series of movements to flip the card inside the flipper
        flipper_position = copy.deepcopy(self.configurations[self.active_configuration].deck)
        flipper_position.position += flipper_offset + Position(x=0, y=-0.05, z=0.075)
        self.arcor2_set_pose(flipper_position)
        flipper_position.position += Position(x=0, y=0.05, z=0)
        self.arcor2_set_pose(flipper_position)
        flipper_position.position += Position(x=0, y=0, z=-0.1)
        self.arcor2_set_pose(flipper_position)
        flipper_position.position += Position(x=0, y=-0.05, z=0)
        self.arcor2_set_pose(flipper_position)
        
        # Card is now flipped and can be seen from camera
        await self.detect_card()
        
        # Rotate robot to the other side so the angle matches the flipper
        flipper_position.orientation = self.rotate(flipper_position.orientation, "x", -50)
        flipper_position.position += Position(x=0, y=0.09, z=0.1)
        self.arcor2_set_pose(flipper_position)
        
        # Pick up the card
        flipper_position.position += Position(x=0, y=0.0, z=-0.01)
        self.arcor2_set_pose(flipper_position)
        self.arcor2_start_vacuum()
        
        flipper_position.position += Position(x=0, y=-0.1, z=0)
        self.arcor2_set_pose(flipper_position)
        
        flipper_position = copy.deepcopy(self.configurations[self.active_configuration].deck)
        flipper_position.position += flipper_offset + Position(x=0, y=-0.1, z=0)
        self.arcor2_set_pose(flipper_position)
        
        self.move_to_deck(-0.2)
    
    async def start(self):
        """Starts the game, users can now play the game
        """
        await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"GAME STARTED"))
        self.cards_in_deck = 52 # Reset deck
        
        self.game_state.status = GameStatus.ROUND_ENDED
        self.game_state.turn = 0
        self.game_state.players[0].status = PlayerStatus.LOBBY_READY

        await self.game.broadcast(self.game_state.model_dump_json())
    
    async def player_ready(self, position):
        """Sets the player status to ready and starts the round if all players are ready
        """
        self.game_state.players[position].status = PlayerStatus.LOBBY_READY
        
        await self.check_ready()
        
    async def check_ready(self):
        """Checks if all players are ready to start the game
        """
        if not PlayerStatus.LOBBY_WAITING in [card.status for card in self.game_state.players.values()]:
            await self.start_round()
            
    async def start_round(self):
        """Starts a new round, deals cards to players and dealer
        """
        await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"New round started"))
        
        self.game_state.status = GameStatus.DEALING
        self.game_state.turn = 0        

        for key, card in self.game_state.players.items():
            if card.status == PlayerStatus.LOBBY_READY:
                self.game_state.players[key] = PlayerState(status=PlayerStatus.PLAYING, hand=[], score=0)
            else:
                self.game_state.players[key] = PlayerState(status=PlayerStatus.DISCONNECTED, hand=[], score=0)

        await self.game.broadcast(self.game_state.model_dump_json())
        
        # DEALING CARDS
        self.move_to_deck(-0.2)
        for i in range(1, self.player_count+1):
            await self.deal_cards(i)
        await self.deal_cards(0)
        for i in range(1, self.player_count+1):
            await self.deal_cards(i)
            
        # UPDATE GAME STATE
        await self.next_player_turn()
            
    async def stop(self):
        """Stops the game, resets the game state and player states
        """
        await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"GAME STOPPED"))
        
        self.game_state.status = GameStatus.NOT_STARTED
        self.game_state.turn = 0
        for key, card in self.game_state.players.items():
            if card.status != PlayerStatus.DISCONNECTED:
                self.game_state.players[key] = PlayerState(status=PlayerStatus.LOBBY_WAITING, hand=[], score=0)
            
        await self.game.broadcast(self.game_state.model_dump_json())
            
    async def next_player_turn(self):
        """Next player's turn
        """
        self.game_state.turn += 1
        if self.game_state.turn > self.player_count:
            self.game_state.turn = 0
            await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Dealer TURN"))
            self.game_state.status = GameStatus.DEALING
            await self.game.broadcast(self.game_state.model_dump_json())
            await self.dealer_turn()
        elif self.game_state.players[self.game_state.turn].status != PlayerStatus.PLAYING:
            await self.next_player_turn()
        elif self.game_state.players[self.game_state.turn].status == PlayerStatus.PLAYING and self.game_state.players[self.game_state.turn].score >= 21:
            await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Player {self.game_state.turn} STAND (Blackjack)"))
            await self.next_player_turn()
        else:  
            await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Player {self.game_state.turn} TURN"))
            self.game_state.status = GameStatus.IN_PROGRESS
            await self.game.broadcast(self.game_state.model_dump_json())
            
    async def hit(self, position):
        """Player hits, deals a card to the player
        """
        
        self.game_state.status = GameStatus.DEALING
        await self.game.broadcast(self.game_state.model_dump_json())
        
        await self.deal_cards(position)
        if self.game_state.players[position].score >= 21:
            await self.next_player_turn()
        else:
            self.game_state.status = GameStatus.IN_PROGRESS
            await self.game.broadcast(self.game_state.model_dump_json())

    async def stand(self):
        """Player stands, moves to the next player's turn
        """
        await self.next_player_turn()

    async def dealer_turn(self):
        """Dealer's turn
        """
        score_players = [player.score for player in self.game_state.players.values() if player.status == PlayerStatus.PLAYING][1::]
        print(score_players)
        if not score_players:
            # Every player disconnected while playing
            pass
        elif min(score_players) > 21:
            await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Every player lost (skipping dealers turn)"))
        else:
            while self.game_state.players[0].score < 17:
                await self.deal_cards(0)
        
        self.game_state.status = GameStatus.ROUND_ENDED
        for key, card in self.game_state.players.items():
            if card.status == PlayerStatus.PLAYING:
                self.game_state.players[key].status = PlayerStatus.LOBBY_WAITING
                
        self.game_state.players[0].status = PlayerStatus.LOBBY_READY
        
        await self.game.broadcast(self.game_state.model_dump_json())
        
        await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Round ended"))
            
    async def deal_cards(self, player):
        """Deals cards to the player or dealer
        """
        
        if self.game_state.players[player].status != PlayerStatus.PLAYING:
            # Skip disconnected players
            return
        
        if self.simulation_mode:
            # Simulate card dealing
            await self.detect_card()
            self.game_state.players[player].hand.append(self.detected_card)
            self.game_state.players[player].score = self.calculate_score(player)
            return
        
        
        #  Pick card based on chosen variant
        if not self.turn_cards:
            await self.detect_card()
            await self.pick_card()
        else:
            await self.detect_card()
            await self.pick_card_turn()
            
        if player == 0:
            # Give card to dealer
            self.move_to_dealer(offset_y=-0.2)
            self.move_to_dealer()
            self.arcor2_stop_vacuum()
            
            self.move_to_dealer(offset_y=-0.2)
        else:
            # Give card to player
            # Moves through center (player 2) - robot always moves on 1 axis this way
            if player != 2:
                self.move_to_player(2, offset_y=-0.2)
                
            self.move_to_player(player, offset_y=-0.2)
            self.move_to_player(player)
            self.arcor2_stop_vacuum()
            self.move_to_player(player, offset_y=-0.2)
            
            if player != 2:
                self.move_to_player(2, offset_y=-0.2)
                
        # Add detected card to player's hand and calculate score
        self.game_state.players[player].hand.append(self.detected_card)
        self.game_state.players[player].score = self.calculate_score(player)
        await self.game.broadcast(self.game_state.model_dump_json())
        
        self.cards_in_deck -= 1
        self.move_to_deck(-0.2)
            
    def move_to_dealer(self, offset_y=0):
        """Moves the robot to the dealer position

        :param offset_y: Offset in the y-axis
        """
        card_number = len(self.game_state.players[0].hand)
        
        position = copy.deepcopy(self.configurations["default"].deck)
        offset = self.configurations[self.active_configuration].offsets["dealer"]
        card_offset = self.configurations[self.active_configuration].offsets["card_offset"]

        position.position += offset + (card_offset * card_number) + Position(x=0, y=offset_y, z=0)

        self.arcor2_set_pose(position)
        
    def move_to_player(self, player, offset_y=0):
        """Moves the robot to the player position

        :param player: Index of the player (0 for dealer, 1-3 for players)
        :param offset_y: Offset in the y-axis
        """
        card_number = len(self.game_state.players[player].hand)
        
        position = copy.deepcopy(self.configurations["default"].deck)
        offset = self.configurations[self.active_configuration].offsets["player"]
        card_offset = self.configurations[self.active_configuration].offsets["card_offset"]
        player_offset = self.configurations[self.active_configuration].offsets["next_player"]

        position.position += offset + (card_offset * card_number) + (player_offset * (player - 1)) + Position(x=0, y=offset_y, z=0)

        self.arcor2_set_pose(position)
            
    def calculate_score(self, player):
        """Calculates the score of the player's hand

        :param player: Index of the player (0 for dealer, 1-3 for players)
        :return: Score of the player's hand
        """
        score = 0
        aces = 0
        for card in self.game_state.players[player].hand:
            if card[0] in ['J', 'Q', 'K']:
                score += 10
            elif card[0] == 'A':
                aces += 1
            else:
                score += int(card[:-1])
        for i in range(aces):
            if score + 11 <= 21:
                score += 11
            else:
                score += 1
        return score
        
        
    def rotate(self, orientation: Orientation, axis, angle) -> Orientation:
        """Rotates the robot's orientation around a given axis by a specified angle

        :param axis: Axis of rotation ('x', 'y', or 'z')
        :param angle: Angle of rotation in degrees
        :return: Rotated Orientation
        """
        r = R.from_quat([
            orientation.x,
            orientation.y,
            orientation.z,
            orientation.w
        ])
        r_rotated = r * R.from_euler(axis, angle, degrees=True)
        rotated_orientation = r_rotated.as_quat()
        
        return Orientation(w=rotated_orientation[3],x=rotated_orientation[0],y=rotated_orientation[1],z=rotated_orientation[2])
    
    def move_rotation(self, axis, angle):
        """Moves the robot on the specified axis by the given angle

        :param axis: Axis of rotation ('x', 'y', or 'z')
        :param angle: Angle of rotation in degrees
        """
        self.pose.orientation = self.rotate(self.pose.orientation, axis, angle)
        
        self.arcor2_set_pose(self.pose)
        
    def move_position(self, offset_x=0, offset_y=0, offset_z=0):
        """Moves the robot to a new position by applying offsets to the current pose

        :param offset_x: Offset in the x-axis, defaults to 0
        :param offset_y: Offset in the y-axis, defaults to 0
        :param offset_z: Offset in the z-axis, defaults to 0
        """
        pose = self.pose
        pose.position.x += offset_x
        pose.position.y += offset_y
        pose.position.z += offset_z
        self.arcor2_set_pose(pose)
        
    

    def save_position_custom(self, key):
        """Saves the current pose as a custom position with the given key

        :param key: Key of the position
        """
        pose = copy.deepcopy(self.pose)
        self.position_custom[key] = pose
        with open("positions_custom.json", "w") as f:
                json.dump({k: v.model_dump() for k, v in self.position_custom.items()}, f, indent=2)

    def move_position_custom(self, key, offset_x=0, offset_y=0, offset_z=0):
        """Moves the robot to a custom position

        :param key: Name of the position
        :param offset_x: Offset in the x-axis, defaults to 0
        :param offset_y: Offset in the y-axis, defaults to 0
        :param offset_z: Offset in the z-axis, defaults to 0
        """
        pose = copy.deepcopy(self.position_custom[key])
        pose.position.x += offset_x
        pose.position.y += offset_y
        pose.position.z += offset_z
        self.arcor2_set_pose(pose)
        
    def delete_position_custom(self, key):
        """Deletes a custom position

        :param key: Name of the position
        """
        if key in self.position_custom:
            del self.position_custom[key]
            with open("positions_custom.json", "w") as f:
                json.dump({k: v.model_dump() for k, v in self.position_custom.items()}, f, indent=2)

    async def create_configuration(self, key):
        """Creates a new configuration (duplicate of the active configuration with a new key)

        :param key: Name of the configuration
        """
        if key not in self.configurations:
            self.configurations[key] = copy.deepcopy(self.configurations[self.active_configuration])
            self.active_configuration = key
            with open("positions.json", "w") as f:
                json.dump({k: v.model_dump() for k, v in self.configurations.items()}, f, indent=2)
                
    async def set_active_configuration(self, key):
        """Sets the active configuration to the given key
        
        :param key: Name of the configuration
        """
        if key in self.configurations:  
            self.active_configuration = key
            await self.logger.log(LogItem(type=LogSeverity.DEBUG, message=f"Active configuration set to {key}"))
        else:
            await self.logger.log(LogItem(type=LogSeverity.ERROR, message=f"Configuration {key} does not exist"))
            
    async def delete_configuration(self, key):
        """Deletes the configuration

        :param key: Name of the configuration
        """
        if key in self.configurations and key != "default":
            del self.configurations[key]
            self.active_configuration = "default"
            with open("positions.json", "w") as f:
                json.dump({k: v.model_dump() for k, v in self.configurations.items()}, f, indent=2)
            await self.logger.log(LogItem(type=LogSeverity.DEBUG, message=f"Configuration {key} deleted"))
                
    async def save_configuration_offsets(self, offsets: dict[str, Position]):
        """ Saves the offsets for the active configuration

        :param offsets: Dictionary of offsets with keys as names and values as Position objects
        """
        self.configurations[self.active_configuration].offsets = offsets
        with open("positions.json", "w") as f:
            json.dump({k: v.model_dump() for k, v in self.configurations.items()}, f, indent=2)
            
    async def save_deck_position(self):
        """Saves the current robot position as the position of the deck in the active configuration
        """
        self.configurations[self.active_configuration].deck = self.pose
        with open("positions.json", "w") as f:
            json.dump({k: v.model_dump() for k, v in self.configurations.items()}, f, indent=2)
            
    def move_to_deck(self, offset_y=0):
        """Moves the robot to the deck position
        
        :param offset_y: Offset in the y-axis, defaults to 0
        """
        deck = copy.deepcopy(self.configurations[self.active_configuration].deck)
        deck.position.y += offset_y
        
        self.arcor2_set_pose(deck)
        
    def move_to_offset_position(self, key, offset_y=0):
        """Moves the robot to the deck position with the specified offset

        :param key: Name of the offset position ("dealer", "player", etc.)
        :param offset_y: Offset in the y-axis, defaults to 0
        """
        deck = copy.deepcopy(self.configurations[self.active_configuration].deck)
        offset = self.configurations[self.active_configuration].offsets[key]
        
        deck.position += offset + Position(x=0, y=offset_y, z=0)
        self.arcor2_set_pose(deck)
            
    def get_scene_positions(self) -> dict[str, list[Position]]:
        """Returns the positions of the deck, dealer, players, and custom positions

        :return: Positions of the deck, dealer, players, and custom positions
        """
        positions = {}

        deck = self.configurations[self.active_configuration].deck.position
        dealer_offset = self.configurations[self.active_configuration].offsets["dealer"]
        
        player_offset = self.configurations[self.active_configuration].offsets["player"]
        next_player_offset = self.configurations[self.active_configuration].offsets["next_player"]
        players = [deck + player_offset + next_player_offset * i for i in range(3)]
        
        positions["deck"] = [deck]
        positions["dealer"] = [deck + dealer_offset]
        positions["players"] = players

        positions["custom"] = [position.position for position in self.position_custom.values()]
        return positions
    
    
    async def screenshot(self):
        """Saves a screenshot of the current camera image
        """
        # Request for camera image
        await self.camera_request.put(None)
        
        # Wait for camera image
        data = await self.camera_images.get()
        self.camera_images.task_done()
        
        image = cv2.imdecode(np.frombuffer(base64.b64decode(data.split(",")[1]), np.uint8), cv2.IMREAD_COLOR)
        
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        os.makedirs("../screenshots", exist_ok=True)
        cv2.imwrite(f"../screenshots/{current_time}.png", image)
        await self.logger.log(LogItem(type=LogSeverity.INFO, message=f"Saving screenshot"))
        
    
    async def detect_card(self):
        """Detects a card from the camera image
        """
        # Class labels for the YOLO model
        classes = ['10♣', '10♦', '10♥', '10♠', '2♣', '2♦', '2♥', '2♠', '3♣', '3♦', '3♥', '3♠', '4♣', '4♦', '4♥', '4♠', '5♣', '5♦', '5♥', '5♠', '6♣', '6♦', '6♥', '6♠', '7♣', '7♦', '7♥', '7♠', '8♣', '8♦', '8♥', '8♠', '9♣', '9♦', '9♥', '9♠', 'A♣', 'A♦', 'A♥', 'A♠', 'J♣', 'J♦', 'J♥', 'J♠', 'K♣', 'K♦', 'K♥', 'K♠', 'Q♣', 'Q♦', 'Q♥', 'Q♠']
        
        if self.simulation_mode:
            # Return random card
            self.detected_card = random.choice(classes)
            return self.detected_card

        # Request for camera image
        await self.camera_request.put(None)
        
        # Wait for camera image
        data = await self.camera_images.get()
        self.camera_images.task_done()
        
        # Decode the base64 image
        image = cv2.imdecode(np.frombuffer(base64.b64decode(data.split(",")[1]), np.uint8), cv2.IMREAD_COLOR)
        
        # Convert image to grayscale and back to colored - lose colors, keep shape
        image = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        

        detect_result = self.card_detector(image, verbose=False)
        result = detect_result[0].boxes.cls.to('cpu').tolist()
        if result:
            # Only one card should be detected, take the first detected object
            self.detected_card = classes[int(result[0])]
        else:
            # No card detected, choose a random card
            self.detected_card = np.random.choice(classes)
            await self.logger.log(LogItem(type=LogSeverity.WARNING, message=f"Card not detected (random card: {self.detected_card})"))
            