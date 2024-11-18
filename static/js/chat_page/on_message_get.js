socket.onmessage = function (event){

    let djangoData = JSON.parse(event.data)
    message = djangoData.websocket_message

    console.log(message)

    switch(message.message_type)
    {
        case "new_message":
            add_new_message(message)
            break;
        case "delete_message":
            delete_message_handler(message.message_id)
            break;
    }
}