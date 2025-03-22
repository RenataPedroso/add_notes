from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''} #deixando o label vazio sem pre preenchimento

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        #em widgets estamos diendo que queremos que o tamanho do campo seja maior que o padrao
        widgets = {'text': forms.Textarea(attrs={'cols':80})}

