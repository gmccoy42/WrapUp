from django.contrib import admin
from .models import Keys, Site, Stories, Rank

# Register your models here.
admin.site.register(Site)
admin.site.register(Rank)
admin.site.register(Stories)
admin.site.register(Keys)
