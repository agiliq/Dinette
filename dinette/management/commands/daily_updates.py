from django.core.management.base import NoArgsCommand
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from mailer import send_html_mail

import datetime

from dinette.models import Ftopics, Reply, DinetteUserProfile

class Command(NoArgsCommand):
    help = """
           Cron job to send daily updates to subscribed users
           Sample cron usage:
           python manage.py daily_updates
           """
    
    def handle_noargs(self, **options):
        site = Site.objects.get_current()
        subject = "Daily Digest: %s" %( site.name)
        from_address = '%s notifications <admin@%s>' %(site.name, site.domain)
        to_address = User.objects.filter(dinetteuserprofile__is_subscribed_to_digest=True).values_list('email', flat=True)
        
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        topics = Ftopics.objects.filter(created_on__gt=yesterday)
        replies = Reply.objects.filter(updated_on__gt=yesterday)
        users = DinetteUserProfile.objects.filter(user__date_joined__gt=yesterday)
        active_users = DinetteUserProfile.objects.filter(user__last_login__gt=yesterday)

        if any([topics, replies, users, active_users]):
            variables = {'site': site, 'topics': topics, 'replies': replies, 'users': users, 'active_users': active_users}
            html_message = render_to_string('dinette/email/daily_updates.html', variables)
            send_html_mail(subject, html_message, html_message, from_address, to_address)

