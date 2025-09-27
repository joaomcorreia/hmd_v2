from django.contrib import admin
from .models import ServiceTag, LocationTag, AIProfile, PromptTemplate, AIContent, AILog

@admin.register(ServiceTag)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name","slug")
    search_fields = ("name","slug")
    prepopulated_fields = {"slug":("name",)}

@admin.register(LocationTag)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name","slug","radius_km")
    search_fields = ("name","slug")
    prepopulated_fields = {"slug":("name",)}

@admin.register(AIProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("owner","plan","languages","max_services","max_locations","auto_publish")
    list_filter  = ("plan","auto_publish")

@admin.register(PromptTemplate)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("key",)
    search_fields = ("key","text")

@admin.register(AIContent)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("profile","service","location","language","kind","is_published","updated_at")
    list_filter  = ("kind","language","is_published")
    search_fields = ("content",)

@admin.register(AILog)
class LogAdmin(admin.ModelAdmin):
    list_display = ("profile","event","created_at")
    readonly_fields = ("created_at",)
