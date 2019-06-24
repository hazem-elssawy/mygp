from django.contrib import admin

from .models import UsedProduct


class UsedProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = UsedProduct

admin.site.register(UsedProduct, UsedProductAdmin)