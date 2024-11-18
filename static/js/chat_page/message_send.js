let message_form = $("#message_form")

$('#submit_btn').click(function () {
    let formData = new FormData(message_form[0])
    let allfiles = message_form.find('input[name="fileImage"]');
    if (allfiles[0]){
        for(var i = 0; i < allfiles[0].files.length; i++){
            formData.append("file_"+i, allfiles[0].files[i]);
        }
    }

    $.ajax({
        type: "post",
        url: chat_new_message_url,
        data: formData,
        contentType: false,
        processData: false,
        success: function(data){},
    });

    document.getElementById("id_text").value = ""
});