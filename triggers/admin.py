from django.contrib import admin

from triggers.models import Trigger
from triggers.models import TriggerEvent


class TriggerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'branch',
        'parallelism',
        'repo_url',
    )
admin.site.register(Trigger, TriggerAdmin)

class TriggerEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'commit',
        'trigger',
        'date_created',
        'date_modified',
    )
admin.site.register(TriggerEvent, TriggerEventAdmin)
