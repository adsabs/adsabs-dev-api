## Metrics Search Requests

To retrieve metrics data for a particular search result set append `/metrics/` to the API search endpoint path.

```
https://api.adsabs.harvard.edu/v1/metrics
```

All requests to the metrics search endpoint must include at least the *&q* query parameter. All parameter values shoud be UTF-8 and url-encoded. For search syntax and descriptions of the fields returned, see the section on search requests.

### Example search result metrics request
```

# Metrics for author "Kurtz, M"
https://api.adsabs.harvard.edu/v1/search/query//metrics/?q=author:"Kurtz,+M"&dev_key=abc123
```

### Example metrics response
```
{
  "meta": {
    "hits": 104,
    "count": 20,
    "query": "author:"Kurtz, M"",
    "qtime": 150,
    "api-version": "0.1.1"
  },
  "results": {
    "all_reads": { overview of reads and download stats for all papers},
    "refereed_reads": { overview of reads and download stats for refereed papers},
    "all_stats": { overview of stats and indexes for all papers},
    "refereed_stats": { overview of stats and indexes for refereed papers},
    "reads_histogram": { histogram of read and normalized read counts},
    "paper_histogram": { histogram of paper and normalized paper counts},
    "citation_histogram": { histogram of citation and normalized citation counts},
    "metrics_series": { time series for a number of indexes},
  }
 }
```
The *meta* section contains information about the query and how it was processed.

* *hits* is the total number of hits in the result set.
* *count* is the number of documents returned in the response
* *query* is the submitted query
* *filters* is the value of any submitted *filter* queries
* *qtime* is the time taken to process the actual search
* *api-version* reflects the version of the API endpoint being used. This value is also returned in the HTTP header *X-API-Version*.

The *results* section of the response will include the actual data of the metrics data.

## Metrics Record Requests

Likewise, to retrieve metrics for a single record append `/metrics/` to the API record endpoint.

### Example search result metrics request
```

# Metrics for 2011ApSSP...1...23K"
http://adslabs.org/adsabs/api/record/2011ApSSP...1...23K/metrics/?dev_key=abc123
```

## Metrics Help

The following overview lists the meanings of the various columns in a number of metrics quantities
* *metrics series* - h, g, i10, tori, m, roq, i100, read10*0.1
* *reads histogram* - reads, refereed reads, normalized reads, normalized refereed reads
* *paper histogram* - paper count, refereed paper count, normalized paper count, normalized refereed paper
* *citation histogram* - all citations, all citations to refereed papers, refereed citations, refereed citations to refereed papers, normalized versions of previous columns 

