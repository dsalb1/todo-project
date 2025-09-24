import logging
from django.contrib.auth import logout
from django.shortcuts import redirect


# Get a logger instance
logger = logging.getLogger(__name__)

# Create your views here.
def logout_view(request):
    logout(request)

    logger.warning("Logging user out.")

    return redirect('accounts:login')
