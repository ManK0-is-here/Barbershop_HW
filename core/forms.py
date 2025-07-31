from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Order
        fields = ['client_name', 'phone', 'master', 'services', 'appointment_date', 'comment']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-select', 'id': 'id_master'}),
            'appointment_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['master'].queryset = Master.objects.filter(is_active=True)

        if 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                self.fields['services'].queryset = Service.objects.filter(masters__id=master_id)
            except (ValueError, TypeError):
                pass

    def clean(self):
        
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        services = cleaned_data.get('services')

        if master and services:
            invalid_services = [s for s in services if s not in master.services.all()]
            if invalid_services:
                service_names = ", ".join([s.name for s in invalid_services])
                raise forms.ValidationError(
                    f"Мастер {master.name} не предоставляет услуги: {service_names}"
                )
        return cleaned_data


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['master', 'rating', 'client_name', 'text', 'photo']
        widgets = {
            'master': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['master'].queryset = Master.objects.filter(is_active=True)
        self.fields['rating'].choices = Review.RATING_CHOICES
