import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, TemplateView

from pages.forms import ContactForm, FeedbackForm

logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class ContactPageView(SuccessMessageMixin, FormView):
    form_class = ContactForm
    template_name = 'pages/contact.html'
    success_url = '/'
    success_message = 'Message sent successfully!'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class FeedbackPageView(SuccessMessageMixin, FormView):
    form_class = FeedbackForm
    template_name = 'pages/feedback.html'
    success_url = '/'
    success_message = 'Feedback sent successfully!'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
