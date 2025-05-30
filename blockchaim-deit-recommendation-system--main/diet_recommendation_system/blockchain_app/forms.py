from django import forms

class HealthForm(forms.Form):
    hospital = forms.CharField(max_length=100)
    doctor = forms.CharField(max_length=100)
    patient = forms.CharField(max_length=100)
    age = forms.IntegerField()
    weight = forms.FloatField()
    height = forms.FloatField()
    issues = forms.CharField(widget=forms.Textarea)
    suggestions = forms.CharField(widget=forms.Textarea)
