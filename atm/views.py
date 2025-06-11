from django.views import generic
from transactions import models

class IndexView(generic.ListView):
    model = models.Transaction
    template_name = "atm/index.html"
    context_object_name = "generic"
    