delete_message_onclick_adding = function(div_message_block)
{
    socket.send(JSON.stringify({
        "message_type": "delete_message",
        "message_id": div_message_block.id.replace("message_n_","")
    }))
}


$('.from_me').click(function(event) {
    var div_message_block = $(event.target).closest(".message_block")[0]
    delete_message_onclick_adding(div_message_block)
});


delete_message_handler = function(message_id)
{
    document.querySelector(`#message_n_${message_id}`).outerHTML = ""
}
