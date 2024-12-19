let send_delete_form_ajax = function() {
        let formElement = $('#delete_form')[0];
        let formData = new FormData(formElement);
        let current_obj =  $(this)
        $.ajax({
            type: "post",
            url: delete_relationship_url + $(this).attr('id'),
            data: formData,
            success: function(data){
                if (data["status"] == "success"){
                    pending_obj = $("#pending_to_list_objects").find('#' + current_obj.attr('id'))

                    if (pending_obj.length > 0)
                        pending_obj.closest(".card")[0].outerHTML = ""

                    if (current_obj.closest(".card").length > 0)
                    {
                        new_part = invite_part

                        current_card = current_obj.closest(".card")
                        current_card.find(".reject_wrapper_block")[0].outerHTML = new_part.replace("some_id", current_obj.attr('id'))
                        current_card.find('.invite_btn').last().on('click', send_invite_form_ajax);
                    }

                    if ($("#pending_to_list_objects").children().length === 0)
                        $("#pending_to_list_objects")[0].insertAdjacentHTML("beforeend", '<p class="text-center">У вас нет исходящих заявок</p>')
                }

            },
            contentType: false,
            processData: false,
        });
}

$('.delete_btn').click(send_delete_form_ajax)