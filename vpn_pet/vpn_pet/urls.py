from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from authentication.views import SignUpView, logout_view, ProfileView, EditProfileView
from sites_management.views import GoToSiteExternalData


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # Overriding some of the allauth's generic views
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/logout/", logout_view, name="logout"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/profile/edit/", EditProfileView.as_view(), name="edit_profile"),
    path("accounts/", include("allauth.urls")),
    path("sites/", include("sites_management.urls", namespace="sites_management")),
    # goToExternalSite requires special routing rules, that are defined below
    path(
        "<slug:slug>", GoToSiteExternalData.as_view(), name="go_to_site_external_data"
    ),
    path(
        "<slug:slug>/<path:extra_route>",
        GoToSiteExternalData.as_view(),
        name="go_to_site_external_data",
    ),
]
