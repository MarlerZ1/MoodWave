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

                    current_obj.closest(".card")[0].outerHTML = ""
                    if ($("#pending_to_list_objects").children().length === 0)
                        $("#pending_to_list_objects")[0].insertAdjacentHTML("beforeend", '<p class="text-center">У вас нет исходящих заявок</p>')


                }

            },
            contentType: false,
            processData: false,
        });
}

$('.delete_btn').click(send_delete_form_ajax)