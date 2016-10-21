# CircleCI Github Trigger

A Django webapp designed to be run on Heroku and used to trigger builds on certain branches of a Github repository in CircleCI with custom build parallelism.

## Installation

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

After the app is deployed, run the following command from the heroku CLI:
    heroku run python manage.py createsuperuser

## Using

* Go to `https://your-app-name.herokuapp.com/admin` and log in
* Create a new Trigger
    * Get the github id for the repository and the web_url via the Github API: https://api.github.com/repos/OWNER/REPO
    * Enter a regex to match on branch name
    * Enter the level of parallel containers that should be used for builds of matched branches
* Verify that the repository webhook was created in Github
* Any commit on a matching branch of a linked repository should create a TriggerEvent and trigger a CircleCI build.  The build_url field on the TriggerEvent object is populated with the CircleCI build url
