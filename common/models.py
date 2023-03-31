from django.db import models


class AbstarctBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
