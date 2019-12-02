import re

from rest_framework import serializers

from .models import (
        Builds,
        Commit,
        ECL,
        Job,
)


class CommitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commit
        exclude = ["id"]


class EclSerializer(serializers.ModelSerializer):

    class Meta:
        model = ECL
        exclude = ["id"]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ["id"]


class BuildSerializer(serializers.ModelSerializer):
    commit = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    ecl = serializers.SerializerMethodField()
    job_name = serializers.SerializerMethodField()

    class Meta:
        model = Builds
        fields = ["passed", "commit", "project", "ecl", "job_name"]

    def get_commit(self, obj):
        return obj.sha.sha

    def get_project(self, obj):
        return obj.sha.project

    def get_ecl(self, obj):
        return obj.ecl.name

    def get_job_name(self, obj):
        return obj.job.name
