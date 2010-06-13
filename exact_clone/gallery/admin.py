from django.contrib import admin
from exact_clone.gallery.models import Category, SecondaryCategory, Photo


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

class SecondaryCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

class PhotoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(SecondaryCategory, SecondaryCategoryAdmin)
admin.site.register(Photo, PhotoAdmin)
