from django.contrib import admin
from .models import TagModel, PostModel, UserCommentModel, CustomUserModel


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_filter = ["author", "date"]
    list_display = ["title", "author", "date"]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "second_name"]


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["name", "second_name", "email"]


class UserCommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post_title"]

    def post_title(slef, obj):
        return obj.post.title

    post_title.short_description = "Tytuł posta:"


admin.site.register(PostModel, PostAdmin)
admin.site.register(CustomUserModel)
admin.site.register(TagModel)
admin.site.register(UserCommentModel, UserCommentAdmin)


# Register your models here.
