from django.contrib.auth.models import User

from django.views import generic

from accounts.models import UserATM

class HomeView(generic.TemplateView):
    template_name = "atm/home.html"

class AboutView(generic.TemplateView):
    template_name = "site/about.html"

class ContactView(generic.TemplateView):
    template_name = "site/contact.html"