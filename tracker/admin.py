#from django.contrib import admin
from django.contrib.gis import admin
from .models import *
class myGeoAdminLocation(admin.ModelAdmin):
    list_display = ('user','latitude','longitude','location','last_fetched')
    list_display_links = ('user','latitude','longitude','location','last_fetched')
    search_fields = ('user','latitude','longitude','location','last_fetched')
    list_per_page = 10


admin.site.register(locationDetail,myGeoAdminLocation)
# Register your models here.
