import kronos
from instagram.utils import InstagramUtils


@kronos.register("0 3 * * *")
def renew_instagram_tokens():
    InstagramUtils.renew_long_lived_tokens()
