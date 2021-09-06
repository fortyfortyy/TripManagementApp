# To jest używane wtedy kiedy chciałbym stworzyć bazowy model User który Profil odnosił
# by się do niego bezpośrednio. Wtedy używam sygnałów
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
#
# from django.contrib.auth.models import User
# from .models import Profile
#
# # TODO do email-a poniżej importy
# from django.core.mail import send_mail
# from django.conf import settings
#
#
# @receiver(post_save, sender=User)
# def createProfile(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         Profile.objects.create(
#             user=user,
#             first_name=user.first_name,
#             username=user.username,
#             email=user.email,
#         )
#
#         # TODO poniżej kolejny future (tworzenia listy znajomych)
#         # FriendList.objects.create(
#         #     user=user,
#         # )
#
#         # TODO do wysyłania powitalnego email-a
#         # subject = 'Welcome to Trip Management App'
#         # message = 'We are glad you are here!'
#         #
#         # send_mail(
#         #     subject,
#         #     message,
#         #     settings.EMAIL_HOST_USER,
#         #     [profile.email],
#         #     fail_silently=False,
#         # )
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
