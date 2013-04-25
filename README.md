# adsabs-dev-api

Developer API service description and example client code. 

For answers to some frequently asked questions check out the [wiki](https://github.com/adsabs/adsabs-dev-api/wiki).

For bugs, feature requests or even random questions feel free to use the [issues](https://github.com/adsabs/adsabs-dev-api/issues) section.

**Table of Contents** 

- [Access](#access)
- [Access Settings](#access-settings)
- [Search Requests](#search-requests)
    - [Example search requests](#example-search-requests)
    - [Example search response](#example-search-response)
- [Record Requests](#record-requests)
    - [Example record requests](#example-record-requests)
    - [Example record response](#example-record-response)
- [Available Fields](#available-fields)
- [Search Syntax](#search-syntax)

## Signup & Access

Access to the ADS data holdings is regulated by the the ADS terms of use, as described in the ADS [Terms of Use](http://doc.adsabs.harvard.edu/abs_doc/help_pages/overview.html#use).

Developers who require regular, automated access to our system are encouraged to contact us to gain access to this API.  Upon reviewing requests for API access, we will issue a developer key which should be used for the intended purpose and must not be further shared.

To obtain access to the ADS Developer API you must do two things:

1. log in to our newest version of the ADS search interface here: [ADS 2.0](http://adslabs.org/adsabs/). You'll need to use your existing "Classic ADS" credentials, or register with Classic ADS if you don't have one.
1. apply for and recieve a *developer token* using our [Signup Form](https://docs.google.com/spreadsheet/viewform?formkey=dFJZbHp1WERWU3hQVVJnZFJjbE05SGc6MQ#gid=0)

**All** API requests must include your developer token in the *&dev_key* parameter.

## Access Settings
```
http://adslabs.org/adsabs/api/settings/?dev_key=...
```
Use this endpoint to view your API access permission settings.

## Search Requests

```
http://adslabs.org/adsabs/api/search/?q=...&dev_key=...
```

All requests to the search endpoint must include at least the *&q* query parameter. All parameter values shoud be UTF-8 and url-encoded. For search syntax and descriptions of the fields returned, see below.

The list of possible parameters is as follows. A "*" indicates a parameter that is not available at the "basic" access level.

#### q
a UTF-8, url-encoded string of <= 1000 characters representing the search query. *q* can be used for both fielded, e.g., *"title:exoplanets"*, and unfielded search. See the list of fields below.

#### fmt
Desired response format. Can be one of 'json' or 'xml'. Default is 'json'.

#### rows
number of results to return. Default is 10 and the max is determined by your API access permissions.

#### start
starting point for returned results (for pagination). Default is 0, max is determined by API access permissions.

#### fl
Specify the fields contained in each returned document. Value should be a comma-separated list of field names. Check the *allowed_fields* shown in your */adsabs/api/settings/* to see what's available.

#### filter
Filter your query results using a particular *field:value* condition. This parameter is repeatable.

* *field* can be any field listed in the field descriptions below
* *value* should be a UTF-8, url-encoded string of <= characters

#### sort
Indicate how you wish the result set sorted. The format is *"TYPE direction"* where *direction* is one of "asc" or "desc", and *TYPE* is one of

* DATE - ordered by publication date
* RELEVANCE - ordered by the document's relevance score calculated during the search
* CITED - ordered by the number of citations
* POPULARITY - ordered by how often the document was "read" over the past 90 days

Example of a properly formated & encoded sort param: "...&sort=CITED+desc..."

#### facet*
Include facet data in the response. This parameter is repeatable. The format is *field[:limit[:mincount]]*, where...

* *field* is the name of the field
* *limit* is an integer specifying how many facet values to return. Default is 100.
* *mincount* is an optional integer specifying the minimum count for a facet value to be included. A *mincount* of "1" will exclude facet values with zero counts.

#### hl*
Include snippets containing highlighted query terms with the returned results. This parameter is repeatable. The format is *field[:count]* where...

* *field* is the field to extract the snippets from
* *count* is an integer specifying how many snippets to return per document

### Example search requests
```
# Simple search for "black holes"
http://adslabs.org/adsabs/api/search/?q=black+holes&dev_key=abc123

# Search for "dark energy", filter by author, sort by citation count
http://adslabs.org/adsabs/api/search/?q=dark+energy&filter=author:"Civano,+F"&sort=CITED+desc&dev_key=abc123

# Same search but only return *bibcode* and *property* values
http://adslabs.org/adsabs/api/search/?q=dark+energy&filter=author:"Civano,+F"&sort=CITED+desc&fl=bibcode,property&dev_key=abc123

# Search for author "Kurtz, M", facet on publication author, year and bibstem
http://adslabs.org/adsabs/api/search/?q=author:"Kurtz,+M"&facet=author&facet=year&facet=bibstem&dev_key=abc123

# Limit a search to only refereed articles
http://adslabs.org/adsabs/api/search/?q=author:"Kurtz,+M"&filter=property:refereed&dev_key=abc123

# Same search but with limit and mincount settings
http://adslabs.org/adsabs/api/search/?q=author:"Kurtz,+M"&facet=author:20:1&facet=year:20:1&facet=bibstem:20:1&dev_key=abc123

# Search for "transiting exoplanets", get 200 rows, include fulltext and abstract highlight snippets
http://adslabs.org/adsabs/api/search/?q=transiting+exoplanets&hl=full&hl=abstract&rows=200&dev_key=abc123

# Same search but get the next 200 rows
http://adslabs.org/adsabs/api/search/?q=transiting+exoplanets&hl=full&hl=abstract&rows=200&start=201&dev_key=abc123
```

### Example search response
```
{
  "meta": {
    "hits": 6160,
    "count": 100,
    "query": "black holes",
    "filters": [],
    "qtime": 4,
    "api-version": "0.1"
  },
  "results": {
    "docs": [
      { 'bibcode': '2012AJ....144..160W', ... },
      ...],
    "facets": {
      "author": [
         "Miller, J",
         53,
         "Fabian, A",
         44,
         ...
      ]
  },
```
The *meta* section contains information about the query and how it was processed.

* *hits* is the total number of hits in the result set.
* *count* is the number of documents returned in the response
* *query* is the submitted query
* *filters* is the value of any submitted *filter* queries
* *qtime* is the time taken to process the actual search
* *api-version* reflects the version of the API endpoint being used. This value is also returned in the HTTP header *X-API-Version*.

The *results* section of the response will include the actual data of the found documents. If search highlight snippets are requested they will be incorporated into the data of each respective document as *highlights*. *facets*, if requested, will contain the facet data separated by field.

## Record Requests
```
http://adslabs.org/adsabs/api/record/<identifier>?dev_key=...
```
Record requests require an identifier in the path of the request URL. Currently this can be either an ADS bibcode, a DOI or an arxiv id. 

Record requests accept the following parameters:

#### fmt
Desired response format. Can be one of 'json' or 'xml'. Default is 'json'.

#### fl
Specify the fields contained in each returned document. Check the *allowed_fields* shown in your */adsabs/api/settings/* to see what's available.

#### hl*
Include snippets containing highlighted query terms with the returned results. This parameter is repeatable. The format is *field[:count]* where...

* *field* is the field to extract the snippets from
* *count* is an integer specifying how many snippets to return per document

#### hlq*
The highlight query, i.e., the terms you wish to see highlighted snippets for in the returned document.

### Example record requests
```
# These are equivalent
http://adslabs.org/adsabs/api/record/2012A&A...542A..16R?dev_key=abc123
http://adslabs.org/adsabs/api/record/arXiv:1204.4485?dev_key=abc123
http://adslabs.org/adsabs/api/record/10.1051/0004-6361/201118723?dev_key=abc123

# Only give me the authors and affiliations
http://adslabs.org/adsabs/api/record/2012A&A...542A..16R?fl=author,aff&dev_key=abc123

# Highlight appearances of "dark energy" in the abstract
http://adslabs.org/adsabs/api/record/2012A&A...542A..16R?hl=abstract&hlq="dark+energy"&dev_key=abc123

```

### Example record response
```
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
```
If highlights are requested they will appear alongside the other document fields. For example,
```
{
    ...
    "highlights": {
       "abstract: [
           " by nilpotent <em>fermionic</em> generators of arbitrary conformal dimension,",
           " are shown to be the $n^{th}$ covariant derivative with respect to flat abelian gauge field of the <em>fermionic</em> fields"
        ]
     },
     ...
  },
```

## Available Fields

This list will likely change a lot as we learn what data users are most interested in. To see the up-to-date list of allowed fields you can do an [Access Settings](#access-settings) request.
* *id* - an internal-only integer id. This value cannot be used as the *<identifier>* portion of a record request.
* *bibcode* - the canonical ADS bibcode identifier for this record
* *bibstem* - the abbreviated name of the journal or publication, e.g., *ApJ*.
* *identifier* - an array of alternative identifiers for the record. May contain alternative bibcodes, DOIs and/or arxiv ids.
* *title* - the title of the record
* *author* - an array of the author names associated with the record
* *pub* - the canonical name of the publication the record appeared in
* *keyword* - an array of normalized and un-normalized keyword values associated with the record
* *abstract* - the abstract of the record
* *aff* - an array of the authors' affiliations
* *property* - an array of miscellaneous flags associated with the record. Possible values include: ARTICLE, REFEREED, NOT_REFEREED, INPROCEEDINGS, OPENACCESS, NONARTICLE, EPRINT, BOOK, PROCEEDINGS, CATALOG, SOFTWARE
* *volume* - volume the record appeared in
* *issue* - issue the record appeared in
* *page* - starting page
* *citation_count* - number of citations the item has received

## Search Syntax

The *q* parameter supports both fielded and unfielded searching:

* *black holes*
* *title:black* *title:holes*

Use quotation marks to indicate phrase searching:

* *"black holes"*
* *title:"black holes"*

Prepend terms with "+" or "-" to indicate inclusion or exclusion:

* *+transiting exoplanets*
* *"dark energy" -"weak lensing"*

The default search uses a boolean "AND" between terms, but you may use "OR" and "AND" in combination with "()" to create more complex queries.

Prefix queries (wildcards) are supported for most fields.
