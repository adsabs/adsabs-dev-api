# adsabs-dev-api

ADS Developer API description. 

For bugs, feature requests or even random questions feel free to use the [issues](https://github.com/adsabs/adsabs-dev-api/issues) section.

**Table of Contents** 

- [Access](#access)
- [Access Settings](#access-settings)
- [Search Requests](search.md)
- [Metrics Requests](metrics.md)

## Mailing List

Announcements and discussion related to the Developer API are available via the Google Group, [adsabs-dev-api](https://groups.google.com/forum/#!forum/adsabs-dev-api). We encourage all API users to subscribe, as the functionality of the API, format of responses, etc., will likely be improving and changing rapidly.

## Clients

The unofficial python client for the API can be found here:

* https://github.com/andycasey/ads

## Signup & Access

Access to the ADS data holdings is regulated by the the ADS terms of use, as described in the ADS [Terms of Use](http://doc.adsabs.harvard.edu/abs_doc/help_pages/overview.html#use).

Developers who require regular, automated access to our system are encouraged to contact us to gain access to this API.  Upon reviewing requests for API access, we will issue a developer key which should be used for the intended purpose and must not be further shared.

To obtain access to the ADS Developer API you must do two things:

1. Create an account and log in to the latest version of the [ADS](https://ui.adsabs.harvard.edu). 
1. Push the "Generate a new key" button under the [user profile](https://ui.adsabs.harvard.edu/#user/settings/token)

All API requests must pass your token in an `Authorization: Bearer <token>` HTTP header.

## Access Settings

Each endpoint is individually rate-limited. API Responses advertise these limits in their response headers:

    X-RateLimit-Limit: 5000
    X-RateLimit-Remaining: 4999
    X-RateLimit-Reset: 1435190400

To increase rate limits, please contact us directly at `adshelp@cfa.harvard.edu`.
