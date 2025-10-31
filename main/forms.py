from django import forms


class TicketForm(forms.Form):
    SUBJECT_CHOICES = [
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    ]

    name = forms.CharField(max_length=250, required=True, label="", widget=forms.TextInput(attrs={
        'placeholder': "نام و نام خانوادگی",
        'class': 'ticket-form-name  form-field',
    }))
    message = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={
        "placeholder": 'متن پیام',
        'class': 'form-message form-field',
    }))
    phone = forms.CharField(required=True, max_length=11, label="", widget=forms.TelInput(attrs={
        'placeholder': 'تلفن همراه',
        'class': 'ticket-form-phone form-field',
    }))
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label="موضوع")

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isdigit() and len(phone) != 11 and not phone[0:1] == '09':
                raise forms.ValidationError("شماره تلفن درست نیست!")
            else:
                return phone

