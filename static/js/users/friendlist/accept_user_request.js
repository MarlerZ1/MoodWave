let send_access_form_ajax = function() {

        let formElement = $('#accept_form')[0];
        let formData = new FormData(formElement);
        let current_obj =  $(this)

        $.ajax({
            type: "post",
            url: accept_relationship_url + $(this).attr('id'),
            data: formData,
            success: function(data){
                if (data["status"] == "success")
                {
                    let card = current_obj.closest(".card")
                    card.find(".accept_wrapper_block").remove()
                    card.find(".resized_part").removeClass('col-md-6').addClass('col-md-8')


                    $("#accepted_list_object")[0].insertAdjacentHTML("beforeend", card[0].outerHTML)
                    card[0].outerHTML = ""
                    $('.delete_btn').last().click(send_reject_form_ajax)

                    if ($("#waiting_list_objects").children().length === 0)
                    {
                        $("#waiting_list_objects")[0].insertAdjacentHTML("beforeend", '<p class="text-center">У вас нет заявок в друзья (</p>')
                    }
                }
            },
            contentType: false,
            processData: false,
        });
}

$('.accept_btn').click(send_access_form_ajax)