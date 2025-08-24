from fastapi import FastAPI, WebSocket, status
from fastapi.middleware.cors import CORSMiddleware

from typing import Dict, List

from models import Pose, Position, Orientation, LogItem, LogSeverity
from dealer import Dealer

app = FastAPI()
dealer = Dealer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket routes
@app.websocket("/ws_player/{position}")
async def ws_players(websocket: WebSocket, position: int):
    await dealer.ws_players(websocket, position)
        
@app.websocket("/ws_camera")
async def websocket_camera(websocket: WebSocket):
    await dealer.ws_camera(websocket)
        
@app.websocket("/ws_log")
async def websocket_logger(websocket: WebSocket):
    await dealer.ws_logger(websocket)

# REST API endpoints
@app.post("/state/start", tags=["Game"])
async def start_game():
    await dealer.start()
    
    await dealer.game.broadcast(dealer.game_state.model_dump_json())
    return status.HTTP_200_OK

@app.post("/state/stop", tags=["Game"])
async def stop_game():
    await dealer.stop()
    
    return status.HTTP_200_OK

@app.post("/state/new_round", tags=["Game"])
async def new_round():
    await dealer.start()
    await dealer.game.broadcast(dealer.game_state.model_dump_json())
    return status.HTTP_200_OK


@app.get("/pose_custom", tags=["Positions"])
async def get_custom_poses() -> List[str]:
    return dealer.position_custom.keys()


@app.delete("/pose_custom/delete/{key}", tags=["Positions"])
async def delete_pose_custom(key: str):
    dealer.delete_position_custom(key)
    return status.HTTP_200_OK

@app.post("/pose_custom/move/{key}", tags=["Positions"])
async def move_pose_custom(key: str) -> Pose:
    if dealer.pose is not None:
        dealer.move_position(offset_y=-0.1)
    dealer.move_position_custom(key, offset_y=-0.1)
    dealer.move_position_custom(key)
    
    return dealer.pose

@app.put("/pose_custom/set/{key}", tags=["Positions"])
async def set_pose_custom(key: str):
    dealer.save_position_custom(key)
    return status.HTTP_200_OK

@app.get("/pose_current", tags=["Movement"])
async def current_pose() -> Pose:
    dealer.arcor2_get_current_pose()
    return dealer.pose

@app.post("/move/position", tags=["Movement"])
async def move(offset_x: float,offset_y: float,offset_z: float) -> Pose:
    dealer.move_position(offset_x=offset_x, offset_y=offset_y, offset_z=offset_z)
    return dealer.pose

@app.post("/move/rotation", tags=["Movement"])
async def move_rotation(axis: str, angle: float) -> Pose:
    dealer.move_rotation(axis, angle)
    return dealer.pose


@app.put("/suction/{state}", tags=["Robot"])
async def suction(state: bool):
    if state:
        dealer.arcor2_start_vacuum()
    else:
        dealer.arcor2_stop_vacuum()
        
    return status.HTTP_200_OK

@app.get("/velocity", tags=["Robot"])
async def get_velocity() -> int:
    velocity = dealer.robot_velocity
    return velocity

@app.put("/velocity/{velocity}", tags=["Robot"])
async def set_velocity(velocity: int):
    dealer.robot_velocity = velocity
    return status.HTTP_200_OK


@app.post("/arcor/start", tags=["Robot"])
async def arcor_start():
    await dealer.arcor2_start()
    return status.HTTP_200_OK

@app.post("/arcor/stop", tags=["Robot"])
async def arcor_start():
    await dealer.arcor2_stop()
    return status.HTTP_200_OK


@app.post("/players/disconnect/{player}", tags=["Players"])
async def disconnect_player(player: int):
    await dealer.game.disconnect(player)
    await dealer.remove_player(player)
    await dealer.game.broadcast(dealer.game_state.model_dump_json())
    return status.HTTP_200_OK


@app.put("/state/flip/{flip}", tags=["Game"])
async def flip(flip: bool):
    dealer.turn_cards = flip
    await dealer.logger.log(LogItem(type=LogSeverity.INFO, message=f"Flip set to {flip}")) 
    return status.HTTP_200_OK

@app.put("/state/simulation/{simulation}", tags=["Game"])
async def simulation(simulation: bool):
    dealer.simulation_mode = simulation    
    await dealer.logger.log(LogItem(type=LogSeverity.INFO, message=f"Simulation set to {simulation}"))
    return status.HTTP_200_OK

@app.get("/configuration/keys", tags=["Configuration"])
async def get_configuration_keys() -> List[str]:
    return list(dealer.configurations.keys())

@app.get("/configuration/offsets", tags=["Configuration"])
async def get_configuration_offsets() -> Dict[str, Position]:
    return dealer.configurations[dealer.active_configuration].offsets

@app.put("/configuration/offsets", tags=["Configuration"])
async def set_configuration_offsets(value: Dict[str, Position]):
    await dealer.save_configuration_offsets(value)
    return status.HTTP_200_OK

@app.put("/configuration/new/{key}", tags=["Configuration"])
async def create_configuration(key: str):
    await dealer.create_configuration(key)
    return status.HTTP_200_OK

@app.put("/configuration/active/{key}", tags=["Configuration"])
async def set_active_configuration(key: str):
    await dealer.set_active_configuration(key)
    return status.HTTP_200_OK

@app.delete("/configuration/delete/{key}", tags=["Configuration"])
async def delete_configuration(key: str):
    await dealer.delete_configuration(key)
    return status.HTTP_200_OK

@app.post("/configuration/deck/move", tags=["Configuration"])
async def move_deck() -> Pose:
    if dealer.pose is not None:
        dealer.move_position(offset_y=-0.1)
    dealer.move_to_deck(offset_y=-0.1)
    dealer.move_to_deck()
    return dealer.pose

@app.put("/configuration/deck/set", tags=["Configuration"])
async def set_deck():
    await dealer.save_deck_position()
    return status.HTTP_200_OK


@app.post("/configuration/offset/{key}", tags=["Configuration"])
async def move_offset(key: str) -> Pose:
    if dealer.pose is not None:
        dealer.move_position(offset_y=-0.1)
    dealer.move_to_offset_position(key, offset_y=-0.1)
    dealer.move_to_offset_position(key)
    return dealer.pose

@app.get("/scene", tags=["Scene"])
async def get_scene_positions() -> Dict[str, List[Position]]:
    return dealer.get_scene_positions()

@app.post("/debug/deal", tags=["Debug"])
async def debug_deal():
    dealer.move_to_deck(-0.2)
    await dealer.deal_cards(0)
    return status.HTTP_200_OK

@app.post("/debug/flip", tags=["Debug"])
async def debug_flip():
    await dealer.pick_card_turn()
    await dealer.game.broadcast(dealer.game_state.model_dump_json())
    return status.HTTP_200_OK

@app.post("/debug/detect", tags=["Debug"])
async def debug_detect():
    await dealer.detect_card()
    await dealer.logger.log(LogItem(type=LogSeverity.INFO, message=f"Detected card: {dealer.detected_card}"))
    
    return status.HTTP_200_OK

@app.post("/debug/screenshot", tags=["Debug"])
async def debug_screenshot() -> str:
    await dealer.screenshot()
    
    return status.HTTP_200_OK
