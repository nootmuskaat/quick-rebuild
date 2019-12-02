import logging as log
from os.path import dirname, join

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Commit, ECL, Job, Builds
from .serializers import BuildSerializer


LOG_FILE=join(dirname(dirname(__file__)), "log")
log.basicConfig(format="%(asctime)s - %(message)s",
                level=log.DEBUG,
                filename=LOG_FILE)


@api_view(["POST"])
def build_passed(request):
    log.info(f"Build Passed received: {request.data}")
    job = Job.objects.get_or_create(name=request.data["job"])[0]
    ecl, new_ecl = ECL.objects.get_or_create(name=request.data["ecl"])
    sha, new_sha = Commit.objects.get_or_create(sha=request.data["commit"],
                                                project=request.data["project"])
    # Update last seen field
    if not new_ecl:
        ecl.save()
    if not new_sha:
        sha.save()

    try:
        build = Builds.objects.get(job=job, ecl=ecl, sha=sha)
    except Builds.DoesNotExist:
        build = Builds.objects.create(passed=True, job=job, ecl=ecl, sha=sha)
    else:
        build.passed = True
    build.save()
    return Response(BuildSerializer(build).data,
                    status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def build_failed(request):
    log.info(f"Build Failed received: {request.data}")
    job = Job.objects.get_or_create(name=request.data["job"])[0]
    ecl, new_ecl = ECL.objects.get_or_create(name=request.data["ecl"])
    sha, new_sha = Commit.objects.get_or_create(sha=request.data["commit"],
                                                project=request.data["project"])
    # Update last seen field
    if not new_ecl:
        ecl.save()
    if not new_sha:
        sha.save()

    try:
        build = Builds.objects.get(job=job, ecl=ecl, sha=sha)
    except Builds.DoesNotExist:
        build = Builds.objects.create(passed=False, job=job, ecl=ecl, sha=sha)
    else:
        build.passed = False
    build.save()
    return Response(BuildSerializer(build).data,
                    status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
def build_status(request):

    def error(msg):
        log.info(f"Build Status expected 404: {msg}")
        return {"error": msg, "passed": False}

    log.info(f"Build Status query: {request.query_params}")
    required_fields = ("job", "ecl", "commit", "project",)
    for field in required_fields:
        if field not in request.query_params:
            return Response(error(f"No '{field}' value provided"),
                            status=status.HTTP_400_BAD_REQUEST)
    try:
        job = Job.objects.get(name=request.query_params["job"])
        ecl = ECL.objects.get(name=request.query_params["ecl"])
        sha = Commit.objects.get(sha=request.query_params["commit"],
                                 project=request.query_params["project"])
    except (Job.DoesNotExist, ECL.DoesNotExist, Commit.DoesNotExist) as exc:
        return Response(error("New Job, ECL, or Commit"),
                        status=status.HTTP_404_NOT_FOUND)
    try:
        build = Builds.objects.get(sha=sha, ecl=ecl, job=job)
    except Builds.DoesNotExist:
        return Response(error("No record for this combination yet"),
                        status=status.HTTP_404_NOT_FOUND)
    log.info(f"Returning status: {BuildSerializer(build).data}")
    return Response(BuildSerializer(build).data)
