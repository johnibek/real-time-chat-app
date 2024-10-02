from django import forms
from .models import GroupMessage, ChatGroup

class ChatMessagesModelForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["body"]
        widgets = {
            "body": forms.TextInput(attrs={"placeholder": "Add message ...", "class": "p-4 text-black", "maxlength": '300', 'autofocus': True})
        }


class NewGroupModelForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Add name...',
                'class': 'p-4 text-black',
                'maxlength': '300',
                'autofocus': True
            })
        }


class ChatroomEditModelForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'class': 'p-4 text-xl font-bold mb-4',
                'maxlength': '300'
            })
        }
