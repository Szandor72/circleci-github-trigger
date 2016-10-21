import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from github3 import login
from triggers.models import Trigger
from triggers.models import TriggerEvent

@receiver(post_save, sender=Trigger)
def create_trigger_webhooks(sender, **kwargs):
    # Skip updates
    if not kwargs['created']:
        return

    trigger = kwargs['instance']
  
    # Initialize repo API 
    github = login(settings.GITHUB_USERNAME, settings.GITHUB_PASSWORD)
    repo = github.repository(trigger.github_owner, trigger.github_repo)

    # Check if webhook exists for repo
    existing = False
    for hook in repo.iter_hooks():
        if hook.config.get('url') == settings.WEBHOOK_URL and 'push' in hook.events:
            existing = True

    # If no webhook, create it 
    if not existing:
        repo.create_hook(
            name = 'web',
            config = {
                'url': settings.WEBHOOK_URL,
                'content_type': 'json',
                'secret': settings.GITHUB_WEBHOOK_SECRET,
            },
        )

@receiver(post_save, sender=TriggerEvent)
def trigger_circle_build(sender, **kwargs):
    # Skip updates
    if not kwargs['created']:
        return

    event = kwargs['instance']

    api_url = 'https://circleci.com/api/v1.1/project/github/{}/{}/tree/{}?circle-token={}'.format(
        event.trigger.github_owner,
        event.trigger.github_repo,
        settings.CIRCLECI_TOKEN,
        event.branch,
    )

    data = {
        'revision': event.commit,
        'parallel': event.trigger.parallelism
    }

    response = requests.post(api_url, json=data)

    try:
        build_url = response.json()['build_url']
        event.build_url = build_url
        event.save()
    except:
        raise Exception(response.content)
