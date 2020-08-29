import requests
from typing import Tuple, Dict
from django.conf import settings
from django.utils.http import urlencode
from instagram.models import InstagramFeed
import datetime
from django.utils import timezone


class InstagramUtils():
    """
    Utilities for the Instagram basic display API.
    https://developers.facebook.com/docs/instagram-basic-display-api/
    """
    _redirect_url = settings.INSTAGRAM_REDIRECT_URL
    _app_id = settings.INSTAGRAM_APP_ID
    _app_secret = settings.INSTAGRAM_APP_SECRET
    _api_base_url = "https://api.instagram.com"
    _graph_base_url = "https://graph.instagram.com"

    @staticmethod
    def _make_api_call(url, type_of_request, params):
        if type_of_request == "GET":
            response = requests.get(url, params)
        elif type_of_request == "POST":
            response = requests.post(url, params)
        else:
            raise ValueError("Invalid type of request: " + type_of_request)

        decoded_response = response.json()

        return decoded_response

    @staticmethod
    def get_authorization_url() -> str:
        """
        Returns the url to Instagram that users has to click to
        authenticate their account.
        """
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
    def _get_short_lived_token(instagram_code: str) -> str:
        """
        Gets a short lived token from instagram with the code
        received from instagram.

        Parameters:

        instagram_code: The code received from instagram

        Returns:

        The short lived access token from Instagram
        """
        post_params = {
            'client_id': InstagramUtils._app_id,
            'redirect_uri': InstagramUtils._redirect_url,
            'client_secret': InstagramUtils._app_secret,
            'grant_type': 'authorization_code',
            'code': instagram_code,
        }

        url = InstagramUtils._api_base_url + "/oauth/access_token"
        response = InstagramUtils._make_api_call(url, "POST", post_params)

        return response.get("access_token")

    @staticmethod
    def get_long_lived_token(instagram_code: str) -> Tuple[str, int]:
        """
        Gets a long lived access token with the code from Instagram.

        Parameters:

        instagram_code: The code received from instagram

        Returns:

        A tuple with the access token and the number of seconds until it
        expires (access_token, expires_in)
        """
        short_lived_token = \
            InstagramUtils._get_short_lived_token(instagram_code)

        get_params = {
            'grant_type': 'ig_exchange_token',
            'client_secret': InstagramUtils._app_secret,
            'access_token': short_lived_token,
        }

        url = InstagramUtils._graph_base_url + "/access_token"
        response = InstagramUtils._make_api_call(url, "GET", get_params)

        return (
            response.get("access_token"),
            response.get("expires_in")
        )

    @staticmethod
    def get_latest_media(account_name: str) -> Dict:
        """
        Gets the latest media from Instagram for the specified account.
        The account must exist in the database and have a vaild access token.

        Parameters:

        account_name: The name of the account.

        Returns:

        A dict with the fields permalink, media_url, media_type, thumbnail_url.
        More details about them are found here:
        https://developers.facebook.com/docs/instagram-basic-display-api/reference/media#fields
        """
        account = InstagramFeed.objects.get(pk=account_name)

        get_params = {
            "fields": "permalink, media_url, media_type, thumbnail_url",
            "access_token": account.access_token,
        }

        url = InstagramUtils._graph_base_url + "/me/media"
        response = InstagramUtils._make_api_call(url, "GET", get_params)

        first_image_dict = response.get("data")[0]

        return first_image_dict

    @staticmethod
    def get_account_name(access_token: str) -> str:
        """
        Gets the name of the account with the associated access_token
        from Instagram.

        Parameters:

        access_token: The access token for the account

        Returns:

        The name of the Instagram account
        """
        get_params = {
            "fields": "username",
            "access_token": access_token,
        }

        url = InstagramUtils._graph_base_url + "/me"
        response = InstagramUtils._make_api_call(url, "GET", get_params)

        return response.get("username")

    @staticmethod
    def renew_long_lived_tokens():
        """
        Refreshes all long lived tokens that will expire in 10 days or earlier.

        More info:
        https://developers.facebook.com/docs/instagram-basic-display-api/guides/long-lived-access-tokens#refresh-a-long-lived-token
        """
        in_ten_days = timezone.now() + datetime.timedelta(days=10)
        feeds_to_renew = InstagramFeed.objects.filter(expires__lte=in_ten_days)

        for feed in feeds_to_renew:
            get_params = {
                "grant_type": "ig_refresh_token",
                "access_token": feed.access_token,
            }

            url = InstagramUtils._graph_base_url + "/refresh_access_token"
            response = InstagramUtils._make_api_call(url, "GET", get_params)

            expires = timezone.now() + \
                datetime.timedelta(seconds=response.get("expires_in"))

            feed.access_token = response.get("access_token")
            feed.expires = expires

            feed.save()
