import logging

from django import forms
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200)
    message = forms.CharField(max_length=600, widget=forms.Textarea)

    def send_mail(self):
        logger.info("sending message...")
        message = "From {0}\nMessage {1}".format(
            self.cleaned_data["name"], self.cleaned_data["message"]
        )
        send_mail(
            subject="Site message",
            message=message,
            from_email="site@domain.con",
            recipient_list=["gurupratap.matharu@gmail.com"],
            fail_silently=False,
        )


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=200)
    message = forms.CharField(max_length=600, widget=forms.Textarea)

    def send_mail(self):
        logger.info("sending feedback...")
        message = "From {0}\nMessage {1}".format(
            self.cleaned_data["name"], self.cleaned_data["message"]
        )
        send_mail(
            subject="Feedback message",
            message=message,
            from_email="site@domain.com",
            recipient_list=["gurupratap.matharu@gmail.com"],
            fail_silently=False,
        )
