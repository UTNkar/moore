# Instagram

This app adds an Instagram block that can be used on websites.
It displayes the latest picture from an instagram account.

Since Instagram is owned by Facebook, we must use Facebook's API which can require some setup and makes the user flow a bit different.

Link to Facebook's API for Instagram: [https://developers.facebook.com/docs/instagram-basic-display-api/](https://developers.facebook.com/docs/instagram-basic-display-api/)

## How the instagram API works

If a user wants to display images from the Instagram, Facebook requires that the user must accept the usage of their profile on our website via their authentication tool.
Once the user has accepted, facebook gives us a short lived token which is valid for 1 hour.
This short lived token can then be exchanged for a long lived token which are valid for 60 days.
With that long lived token we can display the images from the users instagram account.

### How this app uses the API

This app adds a new page under Branding in the admin menu where Instagram feeds can be created.
When you create an Instagram feed you are redirected to facebook authentication.
When you accept, you are redirected back to our site.
The redirect from facebook contains the short lived token.
We exhange this token for a long lived token and save it, along with the account name and expire date in the database.
Now the instagram is available and can be added with the Instagram block on a site.

## Automatic renewal

All long lived tokens are automatically renewed 10 days before they expire.

## Developing and testing Instagram

If you are going to develop or test this app, you have to preform some extra steps.

1. Get access to the UTN app on [developers.facebook.com](developers.facebook.com) by UTN's system administrator.
2. When you have access you must add your personal instagram account as an instagram tester on  [developers.facebook.com](developers.facebook.com). Make sure you do this on the **UTN - Test** app.
3. Install [expose](https://beyondco.de/docs/expose/getting-started/installation) and create an account on their website.
**Explanation**: Facebook needs to redirect the user back to our site when they have agreed. However, when your developing, your server is only available on your computer.
Therefor you must expose it to the internet so that the redirect reaches your development server. This is what expose does.
4. Add your expose token `expose token your-token`
5. Start expose `expose share localhost:8000 --subdomain=moore`.
The subdomain must be set to `moore` since Facebook will redirect to that subdomain.
6. In your `.env-normal` or `.env-docker`, add the Instagram app id, secret key and redirect url.
The app id and secret key are found on the instagarm display block on [developers.facebook.com](developers.facebook.com).
The redirect URL must be exatly the same as the one in the field 'Valid OAuth Redirect URIs'
7. Start your server and go to Branding and you should now be able to start using the Instagram block

