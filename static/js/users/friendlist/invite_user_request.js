let send_invite_form_ajax = function() {
    let formElement = $('#delete_form')[0];
    let formData = new FormData(formElement);
    let current_obj =  $(this)
    $.ajax({
        type: "post",
        url: invite_relationship_url + $(this).attr('id'),
        data: formData,
        success: function(data){
            if (data["status"] == "success"){
                if ($("#pending_to_list_objects").find('p:contains("У вас нет исходящих заявок")').length > 0)
                    $("#pending_to_list_objects").find('p:contains("У вас нет исходящих заявок")')[0].outerHTML = ""

                names = current_obj.closest(".card").find('h6.card-title')[0].innerHTML
                logo_src = current_obj.closest(".card").find('img').attr('src')
                href = current_obj.closest(".card").find('a').attr('href')

                new_part = delete_part_small

                current_card = current_obj.closest(".card")
                current_card.find(".reject_wrapper_block")[0].outerHTML = new_part.replace("some_id", current_obj.attr('id'))
                current_card.find('.delete_btn').last().on('click', send_delete_form_ajax);

                template = $(pending_request_elements)
                template.find('h6.card-title').text(names);
                template.find('img').attr('src', logo_src);
                template.find('a').attr('href', href);
                template.find('.delete_btn').attr('id', current_obj.attr('id'));
                $("#pending_to_list_objects")[0].insertAdjacentHTML("beforeend",  template[0].outerHTML);

                $("#pending_to_list_objects").find(".delete_btn").last().on('click', send_delete_form_ajax);
            }

        },
        contentType: false,
        processData: false,
    });
}