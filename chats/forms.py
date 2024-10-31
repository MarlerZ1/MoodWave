from django import forms

from chats.models import Message, Chat, AttachmentImage


class TextInputForm(forms.Form):
    text = forms.CharField(label="Сообщение...", widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows':"3",
        'style':"resize: none; overflow-y: auto"
    }), required=False)

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': "image_field"

    }), required=False)

    def save(self, **kwargs):
        data = self.cleaned_data


        message = Message(text=data['text'],user=kwargs["user"], chat=Chat.objects.filter(id=kwargs["chat_id"])[0])
        message.save()

        if data['image']:
            attachment_image = AttachmentImage(message=message, image=data['image'])
            attachment_image.save()