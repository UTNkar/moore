from instagram.utils import InstagramUtils
from django.http import HttpResponse


def authenticate(request):
    return HttpResponse(
        "<a href='" +
        InstagramUtils.get_authorization_url() +
        "'>Authenticate</a>"
    )


def get_code(request):
    code = request.GET.get("code")
    image_dict = InstagramUtils.get_latest_image(code)

    return HttpResponse(
        "<p>" + image_dict.get("username") + "</p>" +
        "<a href='" + image_dict.get("permalink") + "'>" +
        "<img src='" + image_dict.get("media_url") + "'/>" +
        "</a>"
    )
