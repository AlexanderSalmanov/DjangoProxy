from django.shortcuts import redirect
from django.db.models import Max
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.views import generic

from .forms import SignUpForm


class SignUpView(generic.CreateView):
    template_name = "account/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        if user:
            login(
                self.request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(SignUpView, self).form_valid(form)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out.")
    return redirect("/")


class ProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = "authentication/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request

        all_sites = request.user.sites.all()
        context["sites_created"] = all_sites.count()
        context["total_site_interactions"] = sum(
            [site.num_transitions for site in all_sites]
        )

        max_transitions = all_sites.aggregate(Max("num_transitions"))
        most_visited_site_obj = all_sites.filter(
            num_transitions=max_transitions["num_transitions__max"]
        ).first()
        context["most_visited_site"] = (
            most_visited_site_obj.name
            if hasattr(most_visited_site_obj, "name")
            else None
        )
        return context


class EditProfileView(LoginRequiredMixin, generic.View):
    def post(self, *args, **kwargs):
        request = self.request
        user = request.user
        email = request.POST.get("change-email")
        full_name = request.POST.get("change-fullname")
        if email:
            user.email = BaseUserManager.normalize_email(email)
        if full_name:
            user.full_name = full_name

        user.save(update_fields=["email", "full_name"])
        messages.success(request, "Profile updated successfully")
        return redirect(reverse_lazy("profile"))
