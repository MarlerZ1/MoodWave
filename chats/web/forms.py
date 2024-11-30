import base64

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

from chats.models import Message, Chat, AttachmentImage, UserInChat
from common.utils.validate_file_type import validate_file_type


class TextInputForm(forms.Form):
    text = forms.CharField(label="Сообщение...", widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows': "3",
        'style': "resize: none; overflow-y: auto"
    }), required=False)

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': "image_field"

    }), required=False)

    def save(self, **kwargs):
        data = self.cleaned_data

        user_ids = [user_in_chat.user.id for user_in_chat in UserInChat.objects.filter(chat_id=kwargs["chat_id"])]

        message = Message(
            text=data['text'],
            user_id=kwargs["user_id"],
            chat=Chat.objects.filter(id=kwargs["chat_id"])[0]
        )

        if data['image']:
            format, imgstr = data['image'][0].split(';base64,')
            ext = format.split('/')[-1]
            try:
                validate_file_type(ContentFile(base64.b64decode(imgstr)))
                has_attach_image = data['image'] != None
            except ValidationError as e:
                has_attach_image = None
                print(e)
                return
            finally:
                if message.text or has_attach_image:
                    message.save(has_attach_image=has_attach_image, user_ids=user_ids)

            attachment_image = AttachmentImage(message=message)

            attachment_image.image.save(
                f'image.{ext}',
                ContentFile(base64.b64decode(imgstr)),
                save=False
            )

            attachment_image.save(user_ids=user_ids)
