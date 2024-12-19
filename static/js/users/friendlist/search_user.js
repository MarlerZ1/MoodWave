const dropdownWrapper = $('.dropdown');
let user_modal_list = $("#userList")
let search_form = $("#search_form")

let send_search_request = function () {
    let formData = new FormData(search_form[0])

    const formObject = Object.fromEntries(formData.entries());
    const queryString = $.param(formObject);

    $.ajax({
        type: "get",
        url: search_user_url,
        data: queryString,
        success: function(data){
            if (data["status"] == "success")
            {
                user_modal_list.empty()
                data["filter"].forEach(couple => {
                    if (couple[1] == "pending")
                        template = delete_friend_small
                    else if (couple[1] == "accept")
                        template = accept_friend_small
                    else if (couple[1] == "rejected")
                        template = reject_friend_small
                    else if (couple[1] == "invite")
                        template = invite_friend_small
                    else if (couple[1] == "waiting")
                        template = waiting_friend_small

                    final_template = template.replace("first_name", couple[0].first_name).replace("last_name", couple[0].last_name).replace("some_id", couple[0].id).replace("some_id", couple[0].id).replace('href', 'href="' + redirect_to_chat_url + couple[0].id + '"')
                    user_modal_list[0].insertAdjacentHTML("beforeend", final_template);


                    if (couple[1] == "pending")
                        user_modal_list.find('.delete_btn').last().on('click', send_delete_form_ajax);
                    else if (couple[1] == "accept")
                        user_modal_list.find('.reject_btn').last().on('click', send_reject_form_ajax);
                    else if (couple[1] == "rejected")
                        user_modal_list.find('.accept_btn').last().on('click', send_access_form_ajax);
                    else if (couple[1] == "invite")
                        user_modal_list.find('.invite_btn').last().on('click', send_invite_form_ajax);
                    else if (couple[1] == "waiting")
                    {
                        user_modal_list.find('.accept_btn').last().on('click', send_access_form_ajax);
                        user_modal_list.find('.reject_btn').last().on('click', send_reject_form_ajax);
                    }
                });
            }
        },
        contentType: false,
        processData: false,
    });
}



search_form.on('submit', function(event) {
    event.preventDefault();
    send_search_request()
});

$('#search_btn').click(function(){
    send_search_request();

    const isExpanded = this.getAttribute('aria-expanded') === 'true';
    if (isExpanded)
        $('#dropdownBackdrop').addClass('show_cst');
    else
       $('#dropdownBackdrop').removeClass('show_cst');
});

dropdownWrapper.click(function(event) {
    event.stopPropagation();
});

$('#dropdownBackdrop').click(function(){
    const isExpanded = this.getAttribute('aria-expanded') === 'true';
    if (!isExpanded) {
        $('#dropdownBackdrop').removeClass('show_cst');
        $('#search_btn')[0].setAttribute('aria-expanded', 'false');
    }
});