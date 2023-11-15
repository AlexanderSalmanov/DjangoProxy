import re
from typing import Union
from django.core.handlers.wsgi import WSGIRequest
from bs4 import BeautifulSoup

from sites_management.models import Site


class TagManager:
    def __init__(self, request, soup, site):
        self.request: WSGIRequest = request
        self.soup: BeautifulSoup = soup
        self.site: Site = site

    def _check_is_relative_url(self, url: str) -> bool:
        """Check if the provided URL is relative or absolute."""
        return url.startswith("/") or not url.startswith("http")

    def _replace_tag_attr(self, tag, attr_name, attr_value):
        """Utility for replacing an attribute in a tag."""
        tag[attr_name] = attr_value

    def _get_stable_relative_url(self, url: str) -> str:
        """Return a relative URL with the site's slug and application's
        base URL prepended to it.
        Used for internal routing."""
        return f"{self.request.build_absolute_uri('/')}{self.site.slug}{url}"

    def _get_stable_absolute_url(self, url: str) -> str:
        """Return an absolute URL with the site's external URL prepended to it.
        Mainly used for images/scripts/stylesheets."""
        return f"{self.site.external_url}{url}"

    def _get_tags(self, tag_names: list[str]):
        """Return a list of tags with the provided names."""
        return self.soup.find_all(tag_names)

    def set_internal_routing(self):
        """Update all the site's relative URLS in `<a>` tag `href` attribute to be routed internally
        within the application."""
        for a_tag in self._get_tags("a"):
            href = a_tag.get("href")
            if href and self._check_is_relative_url(href):
                self._replace_tag_attr(
                    a_tag, "href", self._get_stable_relative_url(href)
                )

    def set_absolute_hrefs(self, tag_names: Union[list[str], str]):
        """Convert all the site's relative URLs to absolute URLs.
        Used to make sure that all the script/stylesheet links are working properly."""
        for tag in self._get_tags(tag_names):
            href = tag.get("href")
            if href and self._check_is_relative_url(href):
                self._replace_tag_attr(tag, "href", self._get_stable_absolute_url(href))
            src = tag.get("src")
            if src and self._check_is_relative_url(src):
                self._replace_tag_attr(tag, "src", self._get_stable_absolute_url(src))
            if tag.name == "img":
                # Ensure that we don't have any confusion between the src and srcset attributes
                self._replace_tag_attr(tag, "srcset", "")

    def set_style_tag_absolute_urls(self):
        """Convert all the site's relative URLs in style tags to absolute URLs."""
        for tag in self._get_tags("style"):
            style_content = tag.string
            if style_content:
                # Use a regular expression to match relative URLs in CSS code
                style_content = re.sub(
                    r'url\(\s*([\'"]?)(/[^\'")]+)\1\s*\)',
                    lambda match: f"url({match.group(1)}{self.site.external_url}{match.group(2)}{match.group(1)})",
                    style_content,
                )
                tag.string = style_content

    def processed_html(self) -> str:
        """Returns the processed HTML as a string."""
        return str(self.soup)
