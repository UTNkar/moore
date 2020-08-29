import requests
from django.conf import settings
from django.utils.http import urlencode
from instagram.models import InstagramFeed
import datetime
from django.utils import timezone


class InstagramUtils():
    _redirect_url = settings.INSTAGRAM_REDIRECT_URL
    _app_id = settings.INSTAGRAM_APP_ID
    _app_secret = settings.INSTAGRAM_APP_SECRET
    _code = ''
    _api_base_url = "https://api.instagram.com"
    _graph_base_url = "https://graph.instagram.com"

    def __init__(self, params_from_instagram):
        self._code = params_from_instagram["code"]

    @staticmethod
    def get_authorization_url():
        get_vars = {
            'app_id': InstagramUtils._app_id,
            'redirect_uri': InstagramUtils._redirect_url,
            'scope': 'user_profile,user_media',
            'response_type': 'code'
        }

        return InstagramUtils._api_base_url + \
            '/oauth/authorize?' + \
            urlencode(get_vars)

    @staticmethod
    def get_short_lived_token(instagram_code):
        post_params = {
            'client_id': InstagramUtils._app_id,
            'redirect_uri': InstagramUtils._redirect_url,
            'client_secret': InstagramUtils._app_secret,
            'grant_type': 'authorization_code',
            'code': instagram_code,
        }

        response = requests.post(
            InstagramUtils._api_base_url + "/oauth/access_token",
            post_params
        )

        decoded_response = response.json()

        return (
            decoded_response.get("access_token"),
            decoded_response.get("user_id")
        )

    @staticmethod
    def get_long_lived_token(instagram_code):
        short_lived_token, user_id = \
            InstagramUtils.get_short_lived_token(instagram_code)

        get_params = {
            'grant_type': 'ig_exchange_token',
            'client_secret': InstagramUtils._app_secret,
            'access_token': short_lived_token,
        }

        response = requests.get(
            InstagramUtils._graph_base_url + "/access_token",
            get_params
        )

        decoded_response = response.json()

        return (
            decoded_response.get("access_token"),
            user_id,
            decoded_response.get("expires_in")
        )

    @staticmethod
    def get_latest_media(account_name):
        account = InstagramFeed.objects.get(pk=account_name)

        get_params = {
            "fields": "permalink, media_url, media_type, thumbnail_url",
            "access_token": account.access_token,
        }

        response = requests.get(
            InstagramUtils._graph_base_url + "/me/media",
            params=get_params
        )

        decoded_response = response.json()

        first_image_dict = decoded_response.get("data")[0]

        return first_image_dict

    @staticmethod
    def get_account_name(access_token):
        get_params = {
            "fields": "username",
            "access_token": access_token,
        }

        response = requests.get(
            InstagramUtils._graph_base_url + "/me",
            params=get_params
        )

        decoded_response = response.json()

        return decoded_response.get("username")

    @staticmethod
    def renew_long_lived_tokens():
        in_ten_days = timezone.now() + datetime.timedelta(days=10)
        feeds_to_renew = InstagramFeed.objects.filter(expires__lte=in_ten_days)

        for feed in feeds_to_renew:
            get_params = {
                "grant_type": "ig_refresh_token",
                "access_token": feed.access_token,
            }

            response = requests.get(
                InstagramUtils._graph_base_url + "/refresh_access_token",
                params=get_params
            )

            decoded_response = response.json()
            expires = timezone.now() + \
                datetime.timedelta(seconds=decoded_response.get("expires_in"))

            feed.access_token = decoded_response.get("access_token")
            feed.expires = expires

            feed.save()
