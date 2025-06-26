from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(max_length = 256,label = "", widget = forms.TextInput(attrs={
        "placeholder": "Повідомлення",
        "class": "message-input"
    }))

class GroupForm(forms.Form):
    class Meta:
        fields = ['name', 'avatar']