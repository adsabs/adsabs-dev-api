## Contents

* [Search API](#search-api)
* [Query parameters](#query-parameters)
* [Fields](#fields)
* [Examples](#example-search-requests)
* [Advanced search syntax](#advanced-search-syntax)


## Search API

Base URL: `https://api.adsabs.harvard.edu/v1/search`

Please note that all queries to the API need to include an HTTP header specifying an access token, e.g.

    curl -H 'Authorization: Bearer <token>' 'https://api.adsabs.harvard.edu/v1/search/query?q=star'

For more information on this please see the top-level [README](README.md) file.

## Get search results

    GET /query?q=value&fl=value2.....

All text values shoud be UTF-8 and url-encoded. The response body will be json encoded.

Note that the search API uses the same syntax as [Apache Solr](http://lucene.apache.org/solr/). For a full reference of query possibilities, please refer to the Solr documentation and [ADS Search Help](http://adsabs.github.io/help/search/). The sections below present useful parameters and patterns for the vast majority of use cases, but are not meant to be exhaustive.


## Parse a query

    GET /qtree?q=this+OR+that

Returns a `query tree` (Abstract Syntax Tree - AST) as understood by our query parser. Useful if you want to modify and/or enhance 
queries.

Example response (value in the `qtree` is a string (JSON) serialized version of the AST):

```
{
             "qtree": "\n{\"name\":\"OPERATOR\", \"label\":\"DEFOP\", \"children\": [\n    {\"name\":\"MODIFIER\", \"label\":\"MODIFIER\", \"children\": [\n        {\"name\":\"TMODIFIER\", \"label\":\"TMODIFIER\", \"children\": [\n            {\"name\":\"FIELD\", \"label\":\"FIELD\", \"children\": [\n                {\"name\":\"QNORMAL\", \"label\":\"QNORMAL\", \"children\": [\n                    {\"name\":\"TERM_NORMAL\", \"input\":\"star\", \"start\":0, \"end\":3}]\n                }]\n            }]\n        }]\n    }]\n}",
             "responseHeader": {
              "status": 0,
              "QTime": 6,
              "params": {
               "q": "star",
               "wt": "json",
               "fl": "id"
              }
             }
            }
```            

## Post a large identifier query

    POST /bigquery[?urlparams]

Returns standard search results, but accepts as input a very large query (i.e. a query that can be expressed only as a list of search
criteria, typically IDs). There is currently no limit to the size of the submitted data (besides buffer/time limits imposed by our API
frontend), however there are severe limits on how often you can call this enpoint. Typically, only 100 requests per day are allowed.

### Parameters

Name          | Type   | Description
--------------|--------|--------------
`urlparams`   |`string`| **Required**. Url escaped/serialized query parameters if used in the URL (ie: `q=star&fl=bibcode,title`) or form encoded search paramaters.
`payload`     |`string`| **Required**. Newline separated list of values, the first line specifies index that will be used for search (ie: `bibcode\n1907AN....174...59.\n1908PA.....16..445.\n1989LNP...334..242S`)


Currently, we allow to search in `bibcode` index only. You can submit `canonical` as well as `alternate` bibcodes; the search will automatically match both. In the future, the list of available indexes may be extended. (We do not plan to support search with other values than IDs).

The bigquery filter is *applied only after* the main search (ie: it limits results of the main search).

Example python session - get all papers from ADS and filter them using several IDs (thus returning only records for the list of input bibcodes):

```python
import requests
bibcodes="bibcode\n1907AN....174...59.\n1908PA.....16..445.\n1989LNP...334..242S"
r = requests.post('https://api.adsabs.harvard.edu/v1/search/bigquery', 
       params={'q':'*:*', 'wt':'json', 'fq':'{!bitset}', 'fl':'bibcode'}, 
       headers={'Authorization': 'Bearer my_token'},
       data=bibcodes)
```

Output is exactly the same as from `/query` endpoint.

  

## Query parameters

All query parameters appearing in the search URL must be UTF-8, url-encoded strings.  Please note that due to the requirements of the authentication library used for validating requests, most non-ascii characters appearing in the URL need to be hex-encoded, e.g. a double quote character (") must be encoded as %22.  In most programming languages the libraries used to retrieve content from web services will perform this encoding for you, but if you are using your own curl-based request you will need to take care of this. 

[Below](#fields) you can find the list of fields available to all API users.  A more comprehensive list is [available in our help pages](https://adsabs.github.io/help/search/comprehensive-solr-term-list).

#### q
*required:* a UTF-8, url-encoded string of <= 1000 characters representing the search query. `q` can be used for both fielded (`title:exoplanets`), and unfielded (`exoplanets`) search. 
#### rows
number of results to return. Default is 10.

#### start
starting point for returned results (for pagination). Default is 0.

#### fl
Fields list: specify the fields contained in each returned document. Value should be a comma-separated list of field names.  Default is just the document id (field `id`).

#### fq
Filter query: filter your results using a particular `field:value` condition. This parameter is repeatable.

* `field` can be any field listed in the field descriptions below
* `value` should be a UTF-8, url-encoded string

#### sort
Indicate how you wish the result set sorted. The format is `field direction` where `direction` is one of `asc` or `desc`, and `field` is a field in the document that contains a numerical value. The default sorting is by relevance (computed by our search engine).

Example of a properly formated & encoded sort param is `sort=read_count+desc`

Some useful fields to sort by may be `pubdate`, `citation_count`, or `first_author`.

## Fields

Below are the fields available to all API users:

* `abstract` - the abstract of the record
* `ack` - the acknowledgements section of an article
* `aff` - an array of the authors' affiliations
* `alternate_bibcode` - list of alternate bibcodes for a single record
* `alternate_title` - list of alternate titles for a single record (usually if they are in multiple languages)
* `arxiv_class` - the arXiv class the pre-print was submitted to
* `author` - an array of the author names associated with the record
* `bibcode` - the canonical ADS bibcode identifier for this record
* `bibgroup` - the bibliographic groups that the bibcode has been associated with
* `bibstem` - the abbreviated name of the journal or publication, e.g., *ApJ*.
* `body`\* - the full text content of the article
* `citation_count` - number of citations the item has received
* `copyright` - the copyright applied to the article
* `data` - the list of sources that have data related to this bibcode
* `database` - Which database the record is associated with.
* `doi`-  the digital object identifier of the article
* `doctype` - the type of document it is (see [here](https://adsabs.github.io/help/search/search-syntax) for a list of doctypes)
* `first_author` - the first author of the article
* `grant` - the list of grant IDs and agencies noted within an article
* `id` - a (**non-persistent**) unique integer for this record, used for fast look-up of a document
* `identifier` - an array of alternative identifiers for the record. May contain alternative bibcodes, DOIs and/or arxiv ids.
* `indexstamp` - time at which the document was (last) indexed
* `issue` - issue the record appeared in
* `keyword` - an array of normalized and un-normalized keyword values associated with the record
* `lang`\* - the language of the article's title
* `orcid_pub` - ORCiD iDs supplied by publishers
* `orcid_user` - ORCiD iDs supplied by knonwn users in the ADS
* `orcid_other` - ORCiD iDs supplied by anonymous users in the ADS
* `page` - starting page
* `property` - an array of miscellaneous flags associated with the record (see [here](https://adsabs.github.io/help/search/search-syntax) for a list of properties
* `pub` - the canonical name of the publication the record appeared in
* `pubdate` - publication date in the form YYYY-MM-DD (DD value will always be "00")
* `read_count` - number of times the record has been viewed within in a 90-day windows (ads and arxiv)
* `title` - the title of the record
* `vizier` - the subject tags given to the article by VizieR
* `volume` - volume the record appeared in
* `year` - the year the article was published

\* *These fields are only indexed and so are only searchable - they are not stored or returned by the search end point, if requested*

#### databases

The ADS content is divided into a few separate databases: "astronomy", "physics" & "general". By default, queries will return results from all three. To limit a search to "astronomy" articles, add `fq=database:astronomy` to the request parameters.

## Example search requests

Assuming your access token is `my_token`, all queries can be executed by any HTTP client. An example `curl` request is:

`curl -H "Authorization: Bearer my_token" "https://api.adsabs.harvard.edu/v1/search/query?........"`

...and by adding the following query params, the response will contain relevant documents:

    # Search by bibcode (make sure you enclose these arguments in quotes!)
    ?q=bibcode:2011ApJ...737..103S

    # Search for "black holes", restricted to astronomy content
    ?q=black+holes&fq=database:astronomy
    
    # Search for "dark energy", filter by author, sort by citation count
    # (double quotes encoded as %22)
    ?q=dark+energy&fq=author:%22Civano,+F%22&sort=citation_count+desc

    # Same search but only return *bibcode* and *property* values
    ?q=dark+energy&fq=author:%22Civano,+F%22&sort=citation_count+desc&fl=bibcode,property

    # Limit a search to only refereed articles
    ?q=author:%22Kurtz,+M%22&fq=property:refereed

    # Search for the phrase "transiting exoplanets", get 200 rows
    ?q=%22transiting+exoplanets%22&rows=200

    # Same search but get the next 200 rows
    ?q=%22transiting+exoplanets%22&rows=200&start=201
    

## Example record response

    {
      "bibcode": "2012A&A...542A..16R",
      "author": [
        "Ranalli, P.",
        "Comastri, A.",
        ...
      ],
      "pub": "Astronomy and Astrophysics",
      "identifier": [
        "2012arXiv1204.4485R",
        "arXiv:1204.4485",
        "2012A&A...542A..16R"
      ],
      "title": "X-ray properties of radio-selected star forming galaxies in the Chandra-COSMOS survey",
      "property": [
        "REFEREED",
        "ARTICLE"
      ],
      "abstract": "X-ray surveys contain sizable numbers of star forming galaxies, ..."
      "keyword": [
        "astronomy x rays",
        "astronomy radio",
        "galaxies fundamental parameters",
        "galaxies star clusters",
        "galaxies active",
        ...
      ],
      "aff": [
        "Università di Bologna, Dipartimento di Astronomia, via Ranzani 1, 40127, Bologna, Italy ; Institute of Astronomy and Astrophysics, National Observatory of Athens, Palaia Penteli, 15236, Athens, Greece; INAF - Osservatorio Astronomico di Bologna, via Ranzani 1, 40127, Bologna, Italy",
        "INAF - Osservatorio Astronomico di Bologna, via Ranzani 1, 40127, Bologna, Italy",
        ...
      ],
    }


## Advanced Search Syntax

The `q` parameter supports both fielded and unfielded searching:

* `black holes`
* `title:black` `title:holes`

Use quotation marks to indicate phrase searching:
    
* `"black holes"`
* `title:"black holes"`

Prepend terms with "+" or "-" to indicate inclusion or exclusion:

* `+transiting exoplanets`
* `"dark energy" -"weak lensing"`

To filter by a publication date range you can use either the `year` or `pubdate` fields:
    
* `pubdate:[2013-07-00 TO *]`
* `pubdate:[2005-01 TO 2007-01]`
* `pubdate:2013-02`
* `year:2013`
* `year:[2012 TO 2013]`

The default search uses a boolean `AND` between terms, but you may use `OR` and `AND` in combination with `()` to create more complex queries.

Prefix queries (wildcards, `*`) are supported for most fields.
