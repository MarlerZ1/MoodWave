add_new_message = function(message) {
    let div = document.querySelector("#list")
    let new_msg = ""
    if (message.from_me){
        new_msg = from_me_msg
        new_msg = new_msg.replace("basicClass", "col-md-2 text-end")
        new_msg = new_msg.replace("basicRef", "img/default_logo.png")
        new_msg = new_msg.replace("messageSender", "from_me")
    } else {
        new_msg = to_me_msg
        new_msg = new_msg.replace("basicRef", "img/default_logo.png")
        new_msg = new_msg.replace("basicClass", "col-md-1")
        new_msg = new_msg.replace("messageSender", "not_from_me")
    }

    new_msg = new_msg.replace("messageId", message.message_id)
    new_msg = new_msg.replace("senderBasic", message.name)
    new_msg = new_msg.replace("messageBasic", message.text)

    if (message.logo_url)
        new_msg = new_msg.replace(default_logo, message.logo_url)

    if (message.image_url)
        new_msg = new_msg.replace("basicAttachmentImage", default_attachment_image.replace(`src=""`,`src="${message.image_url}"`))
    else
        new_msg = new_msg.replace("basicAttachmentImage","")

    div.insertAdjacentHTML("beforeend", new_msg)

    added_object = $("#message_n_" + message.message_id)

    added_object.click(function(){
        delete_message_onclick_adding(this)
    })

}