$('.accept_btn').click(function () {
        let formElement = $('#accept_form')[0];
        let formData = new FormData(formElement);
        let current_obj =  $(this)

        $.ajax({
            type: "post",
            url: accept_relationship_url + $(this).attr('id').replace("accept_",""),
            data: formData,
            success: function(data){
                if (data["status"] == "success")
                {
                    let card = current_obj.closest(".card")
                    card.find(".accept_wrapper_block").remove()
                    card.find(".resized_part").removeClass('col-md-6').addClass('col-md-8')


                    $("#accepted_list_object")[0].outerHTML += card[0].outerHTML
                    card[0].outerHTML = ""

                    if ($("#waiting_list_objects").children().length === 0)
                    {
                        $("#waiting_list_objects")[0].insertAdjacentHTML("beforeend", '<p class="text-center">У вас нет заявок в друзья (</p>')
                    }
                }
            },
            contentType: false,
            processData: false,
        });
    })