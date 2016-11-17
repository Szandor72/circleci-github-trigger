import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class TriggerBuild(BaseCommand):
    help = 'Manually triggers a CircleCI build from the CLI'

    def add_arguments(self, parser):
        parser.add_argument('owner', nargs='+', type=int)
        parser.add_argument('repo', nargs='+', type=int)
        
        parser.add_argument(
            '--branch',
            dest = 'branch',
            default = 'master',
            help = 'Trigger build on a different branch',
        )
        parser.add_argument(
            '--env',
            dest = 'env',
            help = 'Sets the environment variables for the build, ex: VAR1=value1,VAR2=value2',
        )

    def handle(self, owner, repo, **options):
        api_url = 'https://circleci.com/api/v1.1/project/github/{}/{}/tree/{}?circle-token={}'.format(
            owner,
            repo,
            options['branch'],
            settings.CIRCLECI_TOKEN,
        )

        data = {}

        response = requests.post(api_url, json=data)
    
        try:
            build_url = response.json()['build_url']
            print build_url
        except:
            raise CommandError(response.content)
