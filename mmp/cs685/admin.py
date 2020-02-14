from django.contrib import admin
from .models import Tweet, Annotator, Annotation

# Register your models here.
admin.site.register(Tweet)
admin.site.register(Annotator)
admin.site.register(Annotation)
