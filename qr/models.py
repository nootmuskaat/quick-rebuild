from django.core.validators import RegexValidator
from django.db import models


class Commit(models.Model):
    """A commit in one of the project's GIT repos"""
    sha = models.CharField(max_length=40,
                           unique=True,
                           validators=[RegexValidator("^[a-z0-9]{40}$")])
    project = models.CharField(max_length=20)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sha


class Job(models.Model):
    """A Jenkins Job"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ECL(models.Model):
    """
    The ENV VER value of the Environment Control List with which a build is run
    """
    REGEX = "^ENV_VER_[A-Z0-9]+_[0-9]{4}_[0-9]{6}_[0-9]{6}$"
    name = models.CharField(max_length=255,
                            unique=True,
                            validators=[RegexValidator(REGEX)])
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Builds(models.Model):
    """The results of a job built with a given hash and ECL"""
    sha = models.ForeignKey(Commit, related_name="builds", on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name="builds", on_delete=models.CASCADE)
    ecl = models.ForeignKey(ECL, related_name="builds", on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("sha", "job", "ecl"),)
