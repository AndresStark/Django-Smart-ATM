from django.views import generic
from django.urls import reverse_lazy

from .forms import UserATMCreationForm

class RegisterUserView(generic.CreateView):
    form_class = UserATMCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('accounts:login')