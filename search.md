
## Search Requests

All requests to the search endpoint should include at least the *&q* query parameter. All parameter values shoud be UTF-8 and url-encoded. For search syntax and descriptions of the fields returned, see below. The response body will be json encoded.

Note that the search API uses the same syntax as [Apache Solr](http://lucene.apache.org/solr/). For a full reference of query possibilities, please refer to the Solr documentation.

Below is a non-comprehensive list of parameters that may be useful:

#### q
a UTF-8, url-encoded string of <= 1000 characters representing the search query. *q* can be used for both fielded, e.g., *"title:exoplanets"*, and unfielded search. See the list of fields below.

#### rows
number of results to return. Default is 10.

#### start
starting point for returned results (for pagination). Default is 0.

#### fl
Specify the fields contained in each returned document. Value should be a comma-separated list of field names.

#### fq
Filter your query results using a particular *field:value* condition. This parameter is repeatable.

* *field* can be any field listed in the field descriptions below
* *value* should be a UTF-8, url-encoded string

#### sort
Indicate how you wish the result set sorted. The format is *"field direction"* where *direction* is one of "asc" or "desc", and *field* is a field in the document that containers a numerical value. The default sorting is by relevance (computed by our search engine).

Example of a properly formated & encoded sort param: "...&sort=read_count+desc..."

Some useful fields to sort by may be `pubdate`, `citation_count`, or `num_readers`.

### A note about "databases"

The ADS content is divided into a few separate databases: "astronomy", "physics" & "general". By default, the API does not discriminate between them. To limit a search to "astronomy" articles you must add **&fq=database:astronomy** to the request parameters.

### Basic search

    https://api.adsabs.harvard.edu/v1/search/query

### tvrh

    https://api.adsabs.harvard.edu/v1/search/tvrh
    
### qtree

    https://api.adsabs.harvard.edu/v1/search/qtree

### bigquery

    https://api.adsabs.harvard.edu/v1/search/bigquery
    

### Example search requests

Assuming your access token is "my_token", all queries can be executed by any HTTP client. An example `curl` request is:

`curl -H "Authorization: Bearer my_token" https://api.adsabs.harvard.edu/v1/search/query`

...and by adding the following query params, we can find relevant records:

    # Search by bibcode
    ?q=bibcode:2011ApJ...737..103S

    # Search for "black holes", restricted to astronomy content
    ?q=black+holes&filter=database:astronomy
    
    # Search for "dark energy", filter by author, sort by citation count
    ?q=dark+energy&filter=author:"Civano,+F"&sort=citation_count+desc

    # Same search but only return *bibcode* and *property* values
    ?q=dark+energy&filter=author:"Civano,+F"&sort=citation_count+desc&fl=bibcode,property

    # Limit a search to only refereed articles
    ?q=author:"Kurtz,+M"&fq=property:refereed

    # Search for "transiting exoplanets", get 200 rows
    ?q=transiting+exoplanets&rows=200

    # Same search but get the next 200 rows
    ?q=transiting+exoplanets&rows=200&start=201
    

### Example record response

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

## Available Fields

Here are some useful fields that are available to all API users:

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
* *pubdate* - publication date in the form YYYY-MM-DD (DD value will always be "00")

## Advanced Search Syntax

The *q* parameter supports both fielded and unfielded searching:

* *black holes*
* *title:black* *title:holes*

Use quotation marks to indicate phrase searching:

* *"black holes"*
* *title:"black holes"*

Prepend terms with "+" or "-" to indicate inclusion or exclusion:

* *+transiting exoplanets*
* *"dark energy" -"weak lensing"*

To filter by a publication date range you can use either the *year* or *pubdate* fields:

* *pubdate:[2013-07-00 TO *]*
* *pubdate:[2005-01 TO 2007-01]*
* *pubdate:2013-02*
* *year:2013*
* *year:[2012 TO 2013]*
* 
The default search uses a boolean "AND" between terms, but you may use "OR" and "AND" in combination with "()" to create more complex queries.

Prefix queries (wildcards) are supported for most fields.