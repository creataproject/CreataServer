from django.contrib import admin

from apps.sender.models import EmailHistory


@admin.register(EmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):

    search_fields = ['email', 'code', ]
    list_display = ['id', 'email', 'content', 'code', 'created_at', ]
    ordering = ['-created_at', ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False