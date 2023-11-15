from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_by = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="sites"
    )
    external_url = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    data_throughput = models.IntegerField(default=0)
    data_output = models.IntegerField(default=0)
    num_transitions = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.name.lower().replace(" ", "-")
        super(Site, self).save(*args, **kwargs)
