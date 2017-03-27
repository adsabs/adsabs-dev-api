# adsabs-dev-api

ADS Developer API description. 

For bugs, feature requests or even random questions feel free to use the [issues](https://github.com/adsabs/adsabs-dev-api/issues) section.

**Table of Contents** 

- [Access](#access)
- [Access Settings](#access-settings)
- [Search API](search.md)
- [Metrics API](metrics.md)
- [Export API](export.md)
- [Libraries API](libraries.md)

## Mailing List

Announcements and discussion related to the Developer API are available via the Google Group, [adsabs-dev-api](https://groups.google.com/forum/#!forum/adsabs-dev-api). We encourage all API users to subscribe, as the functionality of the API, will likely be improving and changing rapidly.

## Clients

The unofficial python client for the API is maintained by Andy Casey described here:

* http://ads.readthedocs.io/

Examples of how to use Andy Casey's Python client can be found here:

* https://github.com/adsabs/ads-examples

Geert Barentsen has built an application to support the Kepler publication database which uses the ADS API to discover relevant papers:

* https://github.com/KeplerGO/kpub

The ADS built an application to compare author's with a wrestling theme at AAS 227:

* https://authorsmackdown.herokuapp.com/


## Access

Access to the ADS data holdings is regulated by the the ADS terms of use, as described in the ADS [Terms of Use](http://adsabs.github.io/help/terms/).

To obtain access to the ADS Developer API you must do two things:

1. Create an account and log in to the latest version of the [ADS](https://ui.adsabs.harvard.edu). 
1. Push the "Generate a new key" button under the [user profile](https://ui.adsabs.harvard.edu/#user/settings/token)

All API requests must pass your token in an `Authorization: Bearer <token>` HTTP header (where <token> is the key you just generated), e.g.

    curl -H 'Authorization: Bearer <token>' 'https://api.adsabs.harvard.edu/v1/search/query?q=star'


## Access Settings

Each endpoint is individually rate-limited. API Responses advertise these limits in their HTTP response headers.  A useful way to see these values is to issue a curl request to the desired endpoint with the verbose flag, e.g.:

    curl -v -H "Authorization: Bearer <token>" 'https://api.adsabs.harvard.edu/v1/search/query?q=star'
    
And then noting the following values:

    X-RateLimit-Limit: 5000
    X-RateLimit-Remaining: 4999
    X-RateLimit-Reset: 1435190400

The Limit variable indicates the amount of daily queries allowed to the user (in this case 5000).  The Remaining variable indicates how many queries are still available.  The Reset variable provides a UTC timestamp corresponding to the time the rate limits will be reset.  To see its value in human-readable format, you can use the UNIX "date" command:

    date -r 1435190400
    Wed Jun 24 20:00:00 EDT 2015

(the rate resetting happens at midnight UTC).  
To increase rate limits, please contact us directly at `adshelp@cfa.harvard.edu`.
