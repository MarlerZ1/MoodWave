socket.onmessage = function (event){
        let div = document.querySelector("#list")
        let djangoData = JSON.parse(event.data)


        div.innerHTML = ""
        console.log(djangoData)
        for (const i in djangoData.websocket_message){

            newElement =  basicElement

            chat = djangoData.websocket_message.at(i)

            newElement = newElement.replace("BasicCardTitlePlace", chat.name)
            newElement = newElement.replace("BasicCardTextPlace", chat.message_text)
            if (chat.logo)
                newElement = newElement.replace(standart_logo, chat.logo)
            div.innerHTML += newElement
        }

}