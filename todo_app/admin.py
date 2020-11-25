from django.contrib import admin
from todo_app.models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('completed_at',)

admin.site.register(Todo, TodoAdmin)


