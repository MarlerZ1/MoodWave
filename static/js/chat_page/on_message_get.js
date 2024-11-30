socket.onmessage = function (event){
    console.log("socket.onmessage ")
    let djangoData = JSON.parse(event.data)
    message = djangoData.websocket_message

    console.log(message)

    switch(message.message_type)
    {
        case "new_message":
            add_new_message(message)
            break;
        case "delete_message":
            console.log("delete_message signal get")
            delete_message_handler(message.message_id)
            break;
    }
}