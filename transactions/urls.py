from django.urls import path

from .views import WithdrawTransactionFormView, DepositTransactionFormView, TransferTransactionFormView, TransactionVerificationView, TransactionFailedView, TransactionSuccessView

app_name = "transactions"

urlpatterns = [
    path("withdraw/", WithdrawTransactionFormView.as_view(), name="withdraw"),
    path("deposit/", DepositTransactionFormView.as_view(), name="deposit"),
    path("transfer/", TransferTransactionFormView.as_view(), name="transfer"),
    
    path("verification/", TransactionVerificationView.as_view(), name="verification"),
    path("failed/", TransactionFailedView.as_view(), name="failed"),
    path("success/", TransactionSuccessView.as_view(), name="success"),
]