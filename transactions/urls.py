from django.urls import path

from .views import DepositTransactionFormView, TransactionVerificationView, TransactionFailedView, TransactionSuccessView

app_name = "transactions"

urlpatterns = [
    path("deposit/", DepositTransactionFormView.as_view(), name="deposit"),
    path("verification/", TransactionVerificationView.as_view(), name="verification"),
    path("failed/", TransactionFailedView.as_view(), name="failed"),
    path("success/", TransactionSuccessView.as_view(), name="success"),
]