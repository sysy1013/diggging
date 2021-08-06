from django import forms
from django.db.models import fields
from django.db.models.fields import BooleanField, files
from django.forms.widgets import RadioSelect
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {
            "user",
            "title",
            "problem_solving",
            "os",
            "language",
            "error_message",
            "image",
            "desc",
            "tag",
            "code",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"style": "width: 100%", "placeholder": "제목을 입력하세요."}
            ),
            "error_message": forms.TextInput(
                attrs={"sytle": "width: 100%", "placeholder": "발견한 에러메시지를 기록하세요."},
            ),
            "desc": forms.CharField(widget=CKEditorUploadingWidget()),
        }


class selectForm(forms.Form):

    field = forms.ChoiceField(choices=Post.language_choices)
    field2 = forms.ChoiceField(choices=Post.os_choices)
    # field3 = forms.BooleanField(choices=Post.problem_solving)
