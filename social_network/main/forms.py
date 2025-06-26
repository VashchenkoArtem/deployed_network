from django import forms #
from post_app.models import Post, Tag # 
from django.contrib.auth.models import User #


#
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True #
#
class MultipleField(forms.ImageField):
    #
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput()) #
        super().__init__(*args, **kwargs) #
#
    def clean(self, data, initial=None):
        single_file_clean = super().clean #
        if isinstance(data, (list, tuple)): #
            result = [single_file_clean(d, initial) for d in data] #
        else: #
            result = single_file_clean(data, initial) #
        return result #

#
class PostForm(forms.ModelForm):
    #
    class Meta: 
        model = Post #
        fields = ["title", "topic", "tags", "content"] #
    url = forms.URLField( #
        required=False, #
        label="Посилання", #
        widget=forms.URLInput(attrs={ #
            "placeholder": "Вкажіть посилання до публікації", #
            "id": "field-url" #
        })
    )

    title = forms.CharField( #
        max_length=255, # 
        label="Назва публікації", #
        widget=forms.TextInput(attrs={ #
            "placeholder": "Напишіть назву публікації", # 
            "id": "field-title" #
        })
    )

    topic = forms.CharField( #
        max_length=255, #
        required=False, #
        label="Тема публікації", #
        widget=forms.TextInput(attrs={ #
            "placeholder": "Напишіть тему публікації", #
            "id": "field-topic" #
        })
    )

    content = forms.CharField( #
        label="", #
        widget=forms.Textarea(attrs={ #
            "placeholder": "Напишіть текст публікації", #
            "id": "field-text", #
            "class": "text-create", #
        })
    )
    #
    tags = forms.ModelMultipleChoiceField( 
        queryset=Tag.objects.all(), #
        widget=forms.CheckboxSelectMultiple(attrs={"id": "field-tags"}), #
        required=False #
    )

#
class PostFormEdit(forms.ModelForm):
    #
    class Meta(PostForm.Meta): 
        fields = ["title", "topic", "tags", "text", "url"] #

    images = MultipleField(required = False,label = "", widget = MultipleFileInput(attrs = { #
    "id": "image-to-post-form", # 
    "class": "image-to-post-form", #
    "multiple": True #
    }))
    url = forms.URLField(required = False, label = "Посилання", widget= forms.URLInput( #
        {"placeholder": "Вкажіть посилання до публікації"} #
    ))
    title = forms.CharField(max_length= 255,label = "Назва публікації", widget= forms.TextInput( #
        {"placeholder": "Напишіть назву публікації"} #
    ))
    topic = forms.CharField(max_length= 255, required = False,label = "Тема публікації", widget= forms.TextInput( #
        {"placeholder": "Напишіть тему публікації"} #
    ))
    text = forms.CharField(label = "", widget= forms.Textarea( #
        
        {"placeholder": "Напишіть текст публікації"} #
    ))
#
class UserUpdateForm(forms.ModelForm):
    #
    class Meta:
        model = User #
        fields = ['first_name', 'last_name', 'username'] #
        widgets = { #
            'first_name': forms.TextInput(attrs={'class': 'input-name', 'placeholder': "Введіть Ваше ім’я"}), #
            'last_name': forms.TextInput(attrs={'class': 'input-name', 'placeholder': "Введіть Ваше прізвище"}), #
            'username': forms.TextInput(attrs={'class': 'input-name', 'placeholder': "@"}), #
        }

        
