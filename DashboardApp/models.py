from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = CKEditor5Field('Description', config_name='default', blank=True, null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    book_file = models.FileField(upload_to="docs/")
    is_bought = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.price}"