from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from users.forms import UserLoginForm


class UserLoginView(FormView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email_address = form.cleaned_data["email_address"]
        password = form.cleaned_data["password"]
        remember_me = form.cleaned_data.get("remember_me", False)

        user = authenticate(
            self.request, email_address=email_address, password=password
        )

        if user is not None:
            login(self.request, user)
            if remember_me:
                # Set the session to expire in 2 weeks if "remember me" is checked
                self.request.session.set_expiry(1209600)
            else:
                # Keep the session valid until the user closes the browser
                self.request.session.set_expiry(0)

            messages.success(self.request, "You have logged in successfully.")
            return super().form_valid(form)

        form.add_error(None, "Invalid email address or password")
        messages.error(self.request, "Invalid email or password.")
        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
