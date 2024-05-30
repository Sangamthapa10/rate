from django.contrib import admin
from . import models
# Register your models here.


class ModeAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'score')  # Fields to display in the list view

    def thumbnail(self, obj):
        if obj.img:
            return '<img src="{}" width="50" />'.format(obj.img.url)
        else:
            return 'No Image'

    thumbnail.allow_tags = True
    thumbnail.short_description = 'img'

admin.site.register(models.mode, ModeAdmin)

admin.site.register(models.session)

admin.site.register(models.Category)



admin.site.register(models.Type)