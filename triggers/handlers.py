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
    repo = github.repository_with_id(trigger.repo_id)

    # Check if webhook exists for repo
    existing = False
    for hook in repo.hooks():
        if hook.config.get('url') == settings.WEBHOOK_URL and 'push' in hook.events:
            existing = True

    # If no webhook, create it 
    if not existing:
        repo.create_hook(
            name = 'web',
            config = {
                'url': setttings.WEBHOOK_URL,
                'content_type': 'json',
                'secret': settings.WEBHOOK_URL,
            },
        )

@receiver(post_save, sender=TriggerEvent)
def trigger_circle_build(sender, **kwargs):
    # Skip updates
    if not kwargs['created']:
        return

    event = kwargs['instance']

    github = login(settings.GITHUB_USERNAME, settings.GITHUB_PASSWORD)
    repo = github.repository_with_id(event.trigger.repo_id)

    api_url = 'https://circleci.com/api/v1.1/project/gh/{}/{}?circle-token={}'.format(
        repo.owner.login,
        repo.name,
        settings.CIRCLECI_TOKEN,
    )

    data = {
        'revision': event.commit,
        'parallel': event.trigger.parallelism
    }

    response = requests.post(api_url, data)
