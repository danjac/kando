# Django
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

# Kando
from kando.projects.models import ProjectMember


class UserQuerySet(models.QuerySet):
    def for_email(self, email):
        """Returns users matching this email address, including both
        primary and secondary email addresses

        Args:
            email (str): email address

        Returns:
            QuerySet
        """
        return self.filter(
            models.Q(emailaddress__email__iexact=email) | models.Q(email__iexact=email)
        )

    def matches_usernames(self, names):
        """Returns users matching the (case insensitive) username.

        Args:
            names (list): list of usernames

        Returns:
            QuerySet
        """
        if not names:
            return self.none()
        return self.filter(username__iregex=r"^(%s)+" % "|".join(names))


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    def create_user(self, username, email, password=None, **kwargs):
        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        return self.create_user(
            username, email, password, is_staff=True, is_superuser=True, **kwargs,
        )


class User(AbstractUser):
    name = models.CharField(_("Full name"), blank=True, max_length=255)

    objects = UserManager()

    def get_email_addresses(self):
        """Get set of emails belonging to user.

        Returns:
            set: set of email addresses
        """
        return set([self.email]) | set(
            self.emailaddress_set.values_list("email", flat=True)
        )

    @cached_property
    def roles(self):
        """Return projects I own/belong to as dict of {project_id: role}"""
        return {
            m.project_id: m.role
            for m in ProjectMember.objects.filter(user=self, is_active=True)
        }

    def is_member(self, project):
        return project.id in self.roles

    def is_manager(self, project):
        return self.roles.get(project.id) == ProjectMember.Role.MANAGER

    def is_admin(self, project):
        return self.roles.get(project.id) == ProjectMember.Role.ADMIN
