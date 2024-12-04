    $('.delete_btn').click(function () {
        let formElement = $('#delete_form')[0];
        let formData = new FormData(formElement);
        let current_obj =  $(this)

        $.ajax({
            type: "post",
            url: reject_relationship_url + $(this).attr('id').replace("delete_",""),
            data: formData,
            success: function(data){
                if (data["status"] == "success"){

                    current_obj.closest(".card")[0].outerHTML = ""
                    if ($("#waiting_list_objects").children().length === 0)
                        $("#waiting_list_objects")[0].insertAdjacentHTML("beforeend", '<p class="text-center">У вас нет заявок в друзья (</p>')

                    if ($("#accepted_list_object").children().length === 0)
                        $("#accepted_list_object")[0].insertAdjacentHTML("beforeend", '<p class="text-center">У вас все еще нет друзей (</p>')

                }

            },
            contentType: false,
            processData: false,
        });
    })