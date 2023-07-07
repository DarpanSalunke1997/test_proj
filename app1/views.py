from django.shortcuts import render

# Create your views here.

import requests
from ipaddress import ip_address, ip_network
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
import hmac
from hashlib import sha1
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes
from django.views.decorators.http import require_POST
import json
import subprocess


def changes_function(request):
    print("Try 3")
    return HttpResponse(200)


@require_POST
@csrf_exempt
def git_webhook(request):
    # Verify if request came from GitHub
    forwarded_for = "{}".format(request.META.get("HTTP_X_FORWARDED_FOR"))
    client_ip_address = ip_address(forwarded_for)
    whitelist = requests.get("https://api.github.com/meta").json()["hooks"]

    for valid_ip in whitelist:
        if client_ip_address in ip_network(valid_ip):
            break
    else:
        return HttpResponseForbidden("Permission denied.")

    # Verify the request signature
    header_signature = request.META.get("HTTP_X_HUB_SIGNATURE")
    if header_signature is None:
        return HttpResponseForbidden("Permission denied.")

    sha_name, signature = header_signature.split("=")
    if sha_name != "sha1":
        return HttpResponseServerError("Operation not supported.", status=501)

    mac = hmac.new(
        force_bytes(settings.GITHUB_WEBHOOK_KEY),
        msg=force_bytes(request.body),
        digestmod=sha1,
    )
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden("Permission denied.")

    # If request reached this point we are in a good shape
    # Process the GitHub events
    event = request.META.get("HTTP_X_GITHUB_EVENT", "ping")
    print("➡ event :", event)
    print("\n\nbody -- ", request.body)
    if event == "ping":
        return HttpResponse("pong")
    elif event == "pull_request":
        # print("\n\n", request.body, "\n\n", force_bytes(request.body), "\n\n")
        byte_string = request.body
        string = byte_string.decode("utf-8")
        data_dict = json.loads(string)

        if data_dict["action"] == "closed":
            # Deploy some code for example
            script_path = f"{settings.BASE_DIR}/git_test.sh"
            subprocess.run(["bash", script_path])
            return HttpResponse("Success Test Message")

    # In case we receive an event that's not ping or push
    return HttpResponse(status=204)
