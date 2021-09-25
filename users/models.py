from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid


class MyAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password=None):
        """
        Create and save a User with the given email and password and username.
        """
        if not email:
            raise ValueError("User must have an email address.")
        if not username:
            raise ValueError("User must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.is_admin = False
        user.is_superuser = False
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# sends to media_cdn
def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/profile_image.png'


# save to the static
def get_default_profile_image():
    return 'images/profile_images/user-default.png'


class Profile(AbstractUser):

    email = models.EmailField(_('email address'), max_length=60, unique=True)
    short_intro = models.CharField(_('short intro'), max_length=200, null=True, blank=True)
    username = models.CharField(
        _('username'),
        max_length=60,
        unique=True,
        help_text=_('Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    profile_image = models.ImageField(
        max_length=255, blank=True, null=True, upload_to=get_profile_image_filepath, default=get_default_profile_image)
    location = models.CharField(_('location'), max_length=50, null=True, blank=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        """
        Finding an index of image and then take everything towards to the end
        """
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


# TODO in the future friend requests
# class FriendList(models.Model):
#     user = models.OneToOneField(Profile, related_name='user', on_delete=models.CASCADE)
#     friends = models.ManyToManyField(Profile, blank=True, related_name='friends', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.username
#
#     # model dodawania znajomego
#     def add_friend(self, account):
#         if not account in self.friends.all():
#             self.friends.add(account)
#
#     def remove_friend(self, account):
#         """
#         Remove a friend
#         """
#         if account in self.friends.all():
#             self.friends.remove(account)
#
#     def unfriend(self, removee):
#         """
#         Initiate the action of unfriending someone (osoba która odrzuca to removeer, a osoba odrzucona to removee
#         """
#         remover_friend_list = self  # osoba która będzie odrzucała
#
#         # Remove friend from remover friend list
#         remover_friend_list.remove_friend(removee)
#
#         # Remove friend from removee friend list
#         friends_list = FriendList.objects.get(user=removee)
#         friends_list.remove_friend(self.user)
#
#     def is_mutual_friend(self, friend):
#         """
#         Is this a friend?
#         """
#         if friend in self.friends.all():
#             return True
#         return False


# class FriendRequest(models.Model):
#     """
#     A friend request consists of two main parts:
#         1. SENDER:
#             - Person sending/initiating the friend request
#         2. RECEIVER:
#             - Person receiving the friend request
#     """
#     sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
#     receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
#     is_active = models.BooleanField(blank=True, null=False, default=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.sender.username
#
#     def accept(self):
#         """
#         Accept a friend request
#         Update both SENDER and RECEIVER friend lists
#         """
#         receiver_friend_list = FriendList.objects.get(user=self.receiver)
#         if receiver_friend_list:
#             receiver_friend_list.add_friend(self.sender)
#             sender_friend_list = FriendList.objects.get(user=self.sender)
#             if sender_friend_list:
#                 sender_friend_list.add_friend(self.receiver)
#                 self.is_active = False
#
#     def decline(self):
#         """
#         Decline a friend request.
#         It's declined by setting the 'is_active' field to False
#         """
#         self.is_active = False
#
#     def cancel(self):
#         """
#         Cancel a friend request.
#         It's cancelled by setting the 'is_active' field to False.
#         This is only different with respect to "declining" through the notification that is generated.
#         # TODO in the future for notification system
#         """
