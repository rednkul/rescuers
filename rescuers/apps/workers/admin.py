from django.contrib import admin

from .models import Worker, Post, Division, PostState, Service

# Register your models here.

admin.site.site_title = "Административная панель БД ВГСО"
admin.site.site_header = "Административная панель БД ВГСО"

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("id", "surname", "name", "lastname", "post", "division", "on_duty")
    list_display_links = ("id", "surname", "name", "lastname",)
    list_filters = ("division__name", "post__name")
    search_fields = ("surname", "name", "lastname", "division__name", "post__name" )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "operative",  "rescuer",)
    list_display_links = ("id", "name",)
    list_filters = ("rescuer", "operative",)
    search_fields = ("name",)


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    list_display_links = ("id", "name",)
    search_fields = ("name",)

@admin.register(PostState)
class PostStateAdmin(admin.ModelAdmin):
    list_display = ("id", "division", "post")
    list_display_links = ("id", "division", "post")
    search_fields = ("division__name", "post__name")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")