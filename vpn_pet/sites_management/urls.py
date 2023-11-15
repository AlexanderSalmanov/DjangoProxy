from django.urls import path

from . import views


app_name = "sites_management"

urlpatterns = [
    path("delete/<slug:slug>/", views.delete_site, name="delete"),
    path("all/", views.UserSitesView.as_view(), name="user_sites"),
    path("new/", views.CreateNewSite.as_view(), name="create"),
]
