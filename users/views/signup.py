import logging

from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView
from users.forms import SignUpForm

logger = logging.getLogger(__name__)


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()

        # Log the user in
        login(self.request, user)

        # Log the registration event
        logger.info(f"New user registered: {user.email_address}")

        messages.success(self.request, "You have successfully signed up.")

        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning("Signup form invalid")

        messages.error(
            self.request, "There was an error with your signup. Please try again."
        )

        return super().form_invalid(form)
