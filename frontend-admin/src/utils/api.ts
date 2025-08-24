const API_REST_URL = import.meta.env.VITE_API_REST_URL
const API_WS_URL = import.meta.env.VITE_API_WS_URL

console.log('API_REST_URL:', API_REST_URL)
console.log('API_WS_URL:', API_WS_URL)

export const endpoint = (name: string): string => {
    return `${API_REST_URL}${name}`
}

export const websocket = (name: string): WebSocket => {
    return new WebSocket(`${API_WS_URL}${name}`)
}