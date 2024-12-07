let send_access_form_ajax = function() {

        let formElement = $('#accept_form')[0];
        let formData = new FormData(formElement);
        let current_obj =  $(this)
        let obj_id = $(this).attr('id')
        console.log("SEND ACCEPT AJAX")
        if (!formElement) {
            console.error("Форма с ID 'accept_form' не найдена!");
            return;
        }
        $.ajax({
            type: "post",
            url: accept_relationship_url + obj_id,
            data: formData,
            success: function(data){
                if (data["status"] == "success")
                {
                    let card = current_obj.closest(".card")
                    card.find(".accept_wrapper_block").remove()
                    card.find(".resized_part").removeClass('col-md-6').addClass('col-md-8')


                    $("#accepted_list_object")[0].insertAdjacentHTML("beforeend", card[0].outerHTML)
                    card[0].outerHTML = ""
                    let added_object = $("#accepted_list_object").children(':last-child')

                    if (!added_object.find(".reject_btn")[0])
                    {
                        let tempContainer = $('<div>').html(reject_part);
                        tempContainer.find('.reject_btn').attr('id', obj_id);
                        let updatedHtmlString = tempContainer.html();

                        added_object.find('.resized_part:last')[0].insertAdjacentHTML("afterend", updatedHtmlString)
                    }

                    added_object.find('.reject_btn:last').click(send_reject_form_ajax)

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