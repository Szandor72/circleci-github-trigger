import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Manually triggers a CircleCI build from the CLI'

    def add_arguments(self, parser):
        parser.add_argument('owner', nargs='+', type=str)
        parser.add_argument('repo', nargs='+', type=str)
        
        parser.add_argument(
            '--branch',
            dest = 'branch',
            default = 'master',
            help = 'Trigger build on a different branch',
        )
        parser.add_argument(
            '--env',
            action='append',
            dest='env',
            type=lambda kv: kv.split("="),
            help = 'Sets the environment variables for the build, ex: --env VAR1=value1',
        )

    def handle(self, owner, repo, **options):
        api_url = 'https://circleci.com/api/v1.1/project/github/{}/{}/tree/{}?circle-token={}'.format(
            owner[0],
            repo[0],
            options['branch'],
            settings.CIRCLECI_TOKEN,
        )
        data = {}
        if 'env' in options:
            data['build_parameters'] = dict(options['env'])

        response = requests.post(api_url, json=data)
    
        try:
            build_url = response.json()['build_url']
            print build_url
        except:
            raise CommandError(response.content)
