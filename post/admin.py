from django.contrib import admin

from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):

    list_display = ['title','publishing_date','slug']
    list_display_links = ['publishing_date']
    list_filter = ['publishing_date']
    search_fields = ['title']
    list_editable = ['title']

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
