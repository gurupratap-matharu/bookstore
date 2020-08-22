import logging

from django.views.generic import FormView, TemplateView

from pages.forms import ContactForm, FeedbackForm

logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class ContactPageView(FormView):
    form_class = ContactForm
    template_name = 'pages/contact.html'
    success_url = '/'

    def form_valid(self, form):
        logger.info('received valid contact form = %s', form)
        form.send_mail()
        return super().form_valid(form)


class FeedbackPageView(FormView):
    form_class = FeedbackForm
    template_name = 'pages/feedback.html'
    success_url = '/'

    def form_valid(self, form):
        logger.info('Received valid feedback form = %s', form)
        form.send_mail()
        return super().form_invalid(form)
