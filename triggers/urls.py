from django.conf.urls import url

from triggers import views as triggers_views

urlpatterns = [
    url(r'^webhook/github/push$', triggers_views.github_push_webhook),
]
