from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

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
        
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        topics = Ftopics.objects.filter(updated_on__gt=yesterday)
        replies = Reply.objects.filter(updated_on__gt=yesterday)
        users = DinetteUserProfile.objects.filter(user__date_joined__gt=yesterday)
        active_users = DinetteUserProfile.objects.filter(user__last_login__gt=yesterday)

        variables = {'site': site, 'topics': topics, 'replies': replies, 'users': users, 'active_users': active_users}
        html_message = render_to_string('dinette/email/daily_updates.html', variables)
        mail = EmailMessage(subject, html_message, from_address, settings.STAFF_EMAILS)
        mail.content_subtype = "html"
        mail.send()

