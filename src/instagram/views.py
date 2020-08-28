from instagram.utils import InstagramUtils
from instagram.models import InstagramFeed
from django.shortcuts import redirect
import datetime
from django.utils import timezone


def get_code(request):
    code = request.GET.get("code")
    access_token, user_id, expires_in = \
        InstagramUtils.get_long_lived_token(code)

    expires = timezone.now() + datetime.timedelta(seconds=expires_in)

    feed = InstagramFeed.objects.create(
        access_token=access_token,
        expires=expires
    )

    feed.save()

    return redirect("/admin/instagram/instagramfeed/")
