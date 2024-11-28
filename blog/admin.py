from django.contrib import admin
from .models import AuthorModel, TagModel, PostModel


admin.site.register(PostModel)
admin.site.register(AuthorModel)
admin.site.register(TagModel)


# Register your models here.
