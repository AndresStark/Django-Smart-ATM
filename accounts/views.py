from django.views import generic
from django.urls import reverse_lazy
from django.forms import ValidationError

from .forms import UserATMCreationForm, AccountCreationForm
from .models import Account, UserATM

import random

class RegisterUserView(generic.CreateView):
    form_class = UserATMCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('accounts:login')

class AccountDashboardView(generic.ListView):
    model = Account
    template_name = "accounts/dashboard.html"
    context_object_name = "accounts"

class AccountCreationView(generic.FormView):
    form_class = AccountCreationForm
    template_name = 'accounts/creation.html'
    success_url = reverse_lazy('atm:home')

    def form_valid(self, form:AccountCreationForm):
        user = UserATM.objects.get(username=self.request.user.username)
        password = form.obtain_password()
        if user.check_password(password):
            form.instance.user = user
            form.instance.account_number = str(random.randint(10**15, 10**16 - 1))
            form.instance.account_authenticated = True
            form.save()
        else:
            ValidationError('Incorrect password')
        form.save()
        return super().form_valid(form)