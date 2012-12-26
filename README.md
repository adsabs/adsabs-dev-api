# adsabs-dev-api

Developer API service description and example client code

## Access
To obtain access to the ADS Developer API you must first apply for and recieve a *developer token*. Email ???@adslabs.org to obtain a developer token.

**All** API requests must include your developer token in the *&dev_key* parameter.

## Access Settings
```
http://adslabs.org/api/settings/?dev_key=...
```
Use this endpoint to view your API access permission settings.

## Search Results

```
http://adslabs.org/api/search/?dev_key=...
```

All requests to the search endpoint must include at least the *&q* query parameter. Parameter values shoud be UTF-8, url-encoded strings.

The list of possible parameters is as follows:

#### q
a UTF-8, url-encoded string of <= 1000 characters representing the search query
#### fmt
Desired response format. Can be one of 'json' or 'xml'. Default is 'json'.
#### rows
number of results to return. Default is 10 and the max is determined by your API access permissions.
#### start
starting point for returned results (for pagination). Default is 0, max is determined by API access permissions.
#### fl
Desired response field values. Check the *allowed_fields* shown in your */api/settings/* to see what's available.
#### filter
Filter your query results using a particular *field:value* condition. This parameter is repeatable.

* *field* can be any field listed in the field descriptions below
* *value* should be a UTF-8, url-encoded string of <= characters

#### facet*
Include facet data in the response. The format of this parameter is *field[:limit[:mincount]]*, where

* *field* is the name of the field
* *limit* is an integer specifying how many facet values to return
* *mincount* is an optional integer specifying the minimum count for a facet value to be included


## Individual Records
```
http://adslabs.org/api/record/<identifier>?dev_key=...
```

