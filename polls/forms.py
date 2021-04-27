from django import forms
from .models import Comment, Choice, Tag


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea, error_messages={
        'required': 'Please add content in the field'})

    class Meta:
        model = Comment
        fields = ['email', 'body']


class VerifyChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'

    def clean_choice_text(self):
        choice_text = self.cleaned_data['choice_text']
        for instance in Choice.objects.all().exclude(id=self.instance.id):
            if instance.choice_text == choice_text:
                raise forms.ValidationError(
                    'A similar choice already exists: ' + choice_text)
        return choice_text


class VerifyTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def clean_tag(self):
        tag = self.cleaned_data['tag'].lower()
        for instance in Tag.objects.all().exclude(id=self.instance.id):
            if instance.tag.lower() == tag:
                raise forms.ValidationError('A similar tag already exists')
        return tag




