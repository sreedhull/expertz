from django.contrib import admin
from django.utils.html import format_html

from .models import FAQ, Project, Service, SiteSettings

admin.site.site_header = "Expertz Acoustics & Interiors - Admin"
admin.site.site_title = "Expertz Admin"
admin.site.index_title = "Manage your website"


def thumb(obj, field="image"):
    f = getattr(obj, field)
    if f:
        return format_html('<img src="{}" style="height:56px;border-radius:6px;object-fit:cover" />', f.url)
    return "-"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Contact details", {"fields": ("phone_1", "phone_2", "whatsapp_number", "email", "address",
                                        "top_location", "facebook_url", "video_url")}),
        ("Logos", {"fields": ("logo", "logo_light")}),
        ("Big photos", {"fields": ("hero_image", "hero_image_2", "about_image_1", "about_image_2",
                                   "why_image", "cta_image")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Go straight to the one settings record.
        from django.shortcuts import redirect
        obj = SiteSettings.load()
        return redirect("admin:main_sitesettings_change", obj.pk)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("preview", "title", "order", "is_active")
    list_display_links = ("preview", "title")
    list_editable = ("order", "is_active")

    @admin.display(description="Photo")
    def preview(self, obj):
        return thumb(obj)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("preview", "title", "status", "order", "is_active")
    list_display_links = ("preview", "title")
    list_editable = ("status", "order", "is_active")
    list_filter = ("status", "is_active")

    @admin.display(description="Photo")
    def preview(self, obj):
        return thumb(obj)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_active")
    list_editable = ("order", "is_active")
