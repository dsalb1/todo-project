from django import forms

class ToDoForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'name':'title'}), required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'name': 'text'}),  required=True)
    is_completed = forms.BooleanField(required=False)
