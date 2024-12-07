let send_reject_form_ajax = function() {
        let formElement = $('#delete_form')[0];
        let formData = new FormData(formElement);
        let current_obj =  $(this)
        let obj_id = $(this).attr('id')
        console.log("REJECT")
        $.ajax({
            type: "post",
            url: reject_relationship_url + obj_id,
            data: formData,
            success: function(data){
                if (data["status"] == "success"){
                    let card = current_obj.closest(".card")
                    card.find(".reject_wrapper_block").remove()
                    card.find(".resized_part").removeClass('col-md-6').addClass('col-md-8')
                    $("#rejected_list_objects")[0].insertAdjacentHTML("afterbegin", card[0].outerHTML)
                    card[0].outerHTML = ""

                    if ($("#waiting_list_objects").children().length === 0)
                        $("#waiting_list_objects")[0].insertAdjacentHTML("beforeend", '<p class="text-center">У вас нет заявок в друзья (</p>')

                    if ($("#accepted_list_object").children().length === 0)
                        $("#accepted_list_object")[0].insertAdjacentHTML("beforeend", '<p class="text-center">У вас все еще нет друзей (</p>')


                    let added_object = $("#rejected_list_objects").children(':first-child');

                    if (!added_object.find(".accept_btn")[0])
                    {
                        let tempContainer = $('<div>').html(accept_part);
                        tempContainer.find('.accept_btn').attr('id', obj_id);
                        let updatedHtmlString = tempContainer.html();
                        added_object.find('.resized_part:last')[0].insertAdjacentHTML("afterend", updatedHtmlString)
                    }



                    added_object.find('.accept_btn:last').click(send_access_form_ajax)

                }

            },
            contentType: false,
            processData: false,
        });
}

$('.reject_btn').click(send_reject_form_ajax)