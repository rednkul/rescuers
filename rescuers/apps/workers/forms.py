from django import forms

from .models import Worker, Post, Division

class WorkerForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = ['surname', 'name', 'lastname', 'sex', 'post', 'division', 'photo']
        widget = {
            'surname': forms.TextInput(attrs={'class': 'form-control border'}),
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control border'}),
            'sex': forms.RadioSelect(choices=Worker.SEX_CHOICES),
            'post': forms.Select(choices=Post.objects.all()),
            'division': forms.Select(choices=Division.objects.all()),
            'photo': forms.ImageField()
        }