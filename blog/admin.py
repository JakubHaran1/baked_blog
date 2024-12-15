from django.contrib import admin
from .models import AuthorModel, TagModel, PostModel


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_filter = ["author", "date"]
    list_display = ["title", "author", "date"]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "second_name"]


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["name", "second_name", "email"]


admin.site.register(PostModel, PostAdmin)
admin.site.register(AuthorModel)
admin.site.register(TagModel)


# Register your models here.
