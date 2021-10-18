from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.sites.models import Site

#  imports needed for email
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from .models import Profile
from users.utils import account_activation_token


@receiver(post_save, sender=Profile)
def welcomeUserMail(sender, instance, created, **kwargs):
    profile = instance
    if profile.is_active and hasattr(profile, '_sendwelcomemessage'):
        # TODO in the future for creating friends list
        # FriendList.objects.create(
        #     profile=profile,
        # )

        # TODO in the future to send the welcome email
        subject = 'Welcome to Trip Management App'
        message = render_to_string('emails/welcome_email.html', {
            'profile': profile,
        })

        mail = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
        )
        mail.send()


@receiver(post_save, sender=Profile)
def activationUserMail(sender, instance, created, **kwargs):
    profile = instance
    if not profile.is_active and created:

        current_domain = Site.objects.get_current().domain
        subject = 'Activate your account'
        message = render_to_string('emails/activate_account_email.html', {
            'profile': profile,
            'domain': current_domain,
            'uid': urlsafe_base64_encode(force_bytes(profile.pk)),
            'token': account_activation_token.make_token(profile),  # return "%s-%s" % (ts_b36, hash_string)
        })

        mail = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
        )
        mail.send()

#
#
# @receiver(post_save, sender=Profile)
# def updateUser(sender, instance, created, **kwargs):
#     profile = instance
#     user = profile.user
#
#     if not created:
#         user.first_name = profile.first_name
#         user.username = profile.username
#         user.email = profile.email
#         user.save()
#
#
# @receiver(post_delete, sender=Profile)
# def deleteUser(sender, instance, **kwargs):
#     try:
#         user = instance.user
#         user.delete()
#     except:
#         pass
