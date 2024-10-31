from django import forms

from chats.models import Message, Chat


class TextInputForm(forms.Form):
    text = forms.CharField(label="Сообщение...", widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows':"3",
        'style':"resize: none; overflow-y: auto"
    }))

    class Meta:
        model = Message
        fields = ('text')


    def save(self, **kwargs):
        data = self.cleaned_data

        message = Message(text=data['text'],user=kwargs["user"], chat=Chat.objects.filter(id=kwargs["chat_id"])[0])
        message.save()