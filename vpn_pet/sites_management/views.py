import requests
import sys
import logging
from bs4 import BeautifulSoup

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from sites_management.tag_manager import TagManager
from sites_management.models import Site
from sites_management import constants


logger = logging.getLogger(__name__)


class UserSitesView(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        request = self.request
        user = request.user
        sites = user.sites.order_by("-data_throughput")
        return render(request, "sites_management/list.html", {"sites": sites})


class CreateNewSite(LoginRequiredMixin, generic.View):
    def post(self, *args, **kwargs):
        request = self.request
        site_name = request.POST.get("site-name").strip()
        site_url = request.POST.get("site-external-url").lower().strip()

        existing_site_urls_and_names = [
            (external_url, name)
            for external_url, name in Site.objects.values_list("external_url", "name")
        ]
        for url, name in existing_site_urls_and_names:
            if site_url == url or site_name.lower() == name.lower():
                messages.warning(
                    request,
                    f"The site could not be created! "
                    f"A site pointing to {site_url} already exists.",
                )
                return redirect("sites_management:user_sites")

        site = Site(name=site_name, external_url=site_url, created_by=request.user)
        try:
            logger.info(
                f"Attempting to ping a connection to {site_url}. "
                f"Status code: {requests.get(site_url).status_code}"
            )
        except constants.SITE_CREATION_EXCEPTIONS as exc:
            logger.warning(
                f"An error occured on site creation. Context: ", exc_info=exc
            )
            messages.warning(
                request,
                "The site could not be created! "
                f"Reason: {exc.__class__.__name__}. "
                "Double-check the URL and try again.",
            )
            return redirect("sites_management:user_sites")
        else:
            site.save()
        messages.success(request, f"The site {site.name} was created successfully!")
        return redirect("sites_management:user_sites")


@login_required
def delete_site(request, slug):
    site = get_object_or_404(Site, slug=slug)
    if site.created_by != request.user:
        messages.warning(request, "Cannot delete a site that is not yours!")
        return redirect("sites_management:user_sites")
    site.delete()
    messages.success(request, f"The site {site.name} has been successfully deleted.")
    return redirect("sites_management:user_sites")


class GoToSiteExternalData(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        request = self.request
        site_slug = kwargs.get("slug")
        extra_route = kwargs.get("extra_route", None)

        site = Site.objects.get(slug=site_slug, created_by=request.user)
        url = f"{site.external_url}/{extra_route}" if extra_route else site.external_url
        html_data = requests.get(url).text
        soup = BeautifulSoup(html_data, "html.parser")

        tag_mgr = TagManager(request, soup, site)
        tag_mgr.set_absolute_hrefs(constants.DEFAULT_MEDIA_TAGS)
        tag_mgr.set_style_tag_absolute_urls()
        tag_mgr.set_internal_routing()
        processed_html = tag_mgr.processed_html()

        data_sent = request.session["site_data_sent"]["sent_data"]

        site.data_output += data_sent
        site.data_throughput += sys.getsizeof(html_data)
        site.num_transitions += 1
        site.save(update_fields=["data_throughput", "data_output", "num_transitions"])
        return render(
            request,
            template_name="sites_management/external.html",
            context={
                "html_data": processed_html,
            },
        )
