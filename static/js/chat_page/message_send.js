let message_form = $("#message_form")

$('#submit_btn').click(function () {
    let formData = new FormData(message_form[0])
    const formObject = Object.fromEntries(formData.entries());

    let images = [];
    let promises = [];

    const reader = new FileReader();

    for (let [key, value] of formData.entries()) {
        if (value instanceof File) {

            promise = new Promise((resolve, reject) => {
                reader.onload = () => {
                    resolve(reader.result)
                };
                reader.onerror = reject;
                reader.readAsDataURL(value);
            }).then((image) => {
                images.push(image);
            });

            promises.push(promise)
        }
    }

     Promise.all(promises).then(() => {
        socket.send(JSON.stringify({
            "message_type": "send_message",
            "chat_id": chat_id,
            form_data: formObject,
            images_data: images
         }));
     })
    message_form[0].reset()
});