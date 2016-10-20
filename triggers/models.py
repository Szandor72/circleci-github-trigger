from __future__ import unicode_literals

from django.db import models

class Trigger(models.Model):
    repo_id = models.IntegerField()
    repo_url = models.URLField(max_length=255)
    parallelism = models.IntegerField()
    branch = models.CharField(max_length=255)

    @property
    def github_owner(self):
        return self.repo_url.split('/')[3]

    @property
    def github_repo(self):
        return self.repo_url.split('/')[4]

    def __unicode__(self):
        return '({}x) {}/{} {}'.format(
            self.parallelism,
            self.github_owner,
            self.github_repo,
            self.branch,
        )

class TriggerEvent(models.Model):
    trigger = models.ForeignKey(Trigger, related_name='events')
    commit = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
