# adsabs-dev-api

ADS Developer API description. 

For bugs, feature requests or even random questions feel free to use the [issues](https://github.com/adsabs/adsabs-dev-api/issues) section.

**Table of Contents**

The help pages and examples below are formatted as Jupyter notebooks. Browse them in Github or download them to your own computer to edit the code and run as desired. Note that the code in these notebooks was run using an API key or token. This has been edited out of the notebooks for security; [acquire your own API key](#access) and copy it into the notebook before running it locally.

Note: sometimes Github's internal Jupyter notebook rendering agent fails. If that happens, copy the link to the notebook you wish to view into the form at [Jupyter's own notebook renderer](https://nbviewer.jupyter.org/).

- [Access](#access)
- [Access Settings](#access-settings)
- [Search API](Search_API.ipynb)
- [Metrics API](Metrics_API.ipynb)
- [Export API](Export_API.ipynb)
- [Libraries API](Libraries_API.ipynb)
- [Converting curl to Python - examples](Converting_curl_to_python.ipynb)

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

	# syntax for UNIX on a Mac
    date -r 1435190400
	# Linux syntax
	date -d @1435190400
	# output for either
    Wed Jun 24 20:00:00 EDT 2015

(the rate resetting happens at midnight UTC).  
For more information and tips about rate limits, please contact us directly at `adshelp@cfa.harvard.edu`.
