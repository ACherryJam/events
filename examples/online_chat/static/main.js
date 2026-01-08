class DeferredPromise {
    constructor() {
        var self = this
        this.promise = new Promise((resolve, reject) => {
            self.resolve = resolve
            self.reject = reject
        })
    }
}

function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

const connection_form = document.getElementById("connection_form")
const connection_data = document.getElementById("connection_data")
const username_text = document.getElementById("username_text")

const room_input = document.getElementById("room")
const message_input = document.getElementById("message")
const username_input = document.getElementById("username")

message_input.addEventListener("keydown", (event) => {
    if (event.keyCode == 13) {
        on_send()
    }
})

const button_element = document.getElementById("send")
const chat_element = document.getElementById("chat")

var socket = null

var pending_requests = new Map()

function generate_request_id() {
    let minimum = 10000000
    let maximum = 99999999

    let id = Math.floor(
        Math.random() * (maximum - minimum) + minimum
    )
    return String(id)
}

function send_ws_request(data) {
    let request_id = generate_request_id()
    pending_requests.set(request_id, new DeferredPromise())

    data.request_id = request_id
    socket.send(
        JSON.stringify(data)
    )
    console.log(data, "sent")
    
    return pending_requests.get(request_id)
}

function on_user_connect() {
    connection_form.hidden = true
    connection_data.hidden = false
    username_text.innerHTML = username_input.value
}

function on_user_disconnect() {
    connection_form.hidden = false
    connection_data.hidden = true
}

function connect_to_room() {
    let room_id = room_input.value
    let username = username_input.value

    socket = new WebSocket(`/chat?room_id=${room_id}&username=${username}`)

    socket.addEventListener("open", (event) => {
        on_user_connect()
    })

    socket.addEventListener("close", async (event) => {
        socket = null
        on_user_disconnect()
    })

    socket.addEventListener("message", (event) => {
        let response = JSON.parse(event.data)
        
        console.log(response)

        if (response.type == "message") {
            const item = document.createElement("li")
            item.innerText = response.text

            chat_element.appendChild(item)
        }

        if (response.type == "user_connected") {
            const item = document.createElement("li")
            item.innerHTML = `${response.username} connected.`
            item.style.fontStyle = "italic"

            chat_element.appendChild(item)
        }

        if (response.type == "user_disconnected") {
            const item = document.createElement("li")
            item.innerHTML = `${response.username} disconnected.`
            item.style.fontStyle = "italic"

            chat_element.appendChild(item)
        }

        if (response.type == "result") {
            let request_id = response.request_id
            let request = pending_requests.get(request_id)
            request.resolve(response.result === "ok")
        }
    })
}

function disconnect_from_room() {
    if (socket !== null) {
        socket.close()
        socket = null
    }
}

function on_connection_form_submit(event) {
    event.preventDefault()

    connect_to_room()
    return false
}

function on_send() {
    let text = message_input.value
    message_input.value = ""
    
    send_message(text)
}

function send_message(message) {
    if (message == "")
        return
    
    send_ws_request({
        "type": "message",
        "text": message
    })
}