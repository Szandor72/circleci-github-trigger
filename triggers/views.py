import hmac
import json
import re
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from triggers.models import Trigger
from triggers.models import TriggerEvent

def validate_github_webhook(request):
    key = settings.GITHUB_WEBHOOK_SECRET
    signature = request.META.get('HTTP_X_HUB_SIGNATURE').split('=')[1]
    if type(key) == unicode:
        key = key.encode()
    mac = hmac.new(key, msg=request.content, digestmod=sha1)
    if not compare_digest(mac.hexdigest(), signature):
        return False
    return True

@csrf_exempt
@require_POST
def github_push_webhook(request):
    if not validate_github_webhook(request):
        return HttpResponseForbidden

    push = json.loads(request.content)
    repo_id = push['repository']['id']
    
    triggers = Trigger.objects.filter(repo_id = repo_id)
    
    for trigger in triggers:
        # Check if the branch matches the trigger's branch regex 
        branch = push['after'].replace('refs/heads/','')
        if re.findall(trigger.branch, branch): 
            # Trigger the build event
            event = TriggerEvent(
                trigger = trigger,
                commit = push['after'],
            )
            event.save() 

    return HttpResponse('OK')
