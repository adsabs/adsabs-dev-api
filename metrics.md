## Metrics Search Requests

To retrieve metrics data for a particular search result set append `/metrics/` to the API search endpoint path.

```
https://api.adsabs.harvard.edu/v1/metrics
```

If you do a request from the command line like

	curl -H "Authorization: Bearer <your API token>" -H "Content-Type: application/json" -X POST -d '{"bibcodes":["1980ApJS...44..137K","1980ApJS...44..489B"]}' https://api.adsabs.harvard.edu/v1/metrics

and you should get back all metrics data. If you access the API using the Python `requests` module, you would do something like

    r = requests.post(queryURL, data=json.dumps(payload), headers=headers)

where

    payload = {'bibcodes': [bibcode1, bibcode2, ...]}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':'Bearer %s' % token}

and `token` is your API token.

You can also request a specific set of metrics by adding the `types` parameter in the JSON header. For example:

    curl -H "Authorization: Bearer <your API token>" -H "Content-Type: application/json" -X POST -d '{"bibcodes":["1980ApJS...44..137K","1980ApJS...44..489B"],"types":["basic"]}' https://api.adsabs.harvard.edu/v1/metrics

which will return just the basic statistics for the set of bibcodes. The following values are allowed for the `types` list:

  * 'basic': publication and usage stats (all papers, and just refereed papers)
  * 'citations': citation stats
  * 'indicators': indicators, like the h-index, g-index, m-index etc etc
  * 'histograms': publication, citation, reads and downloads histograms
  * 'timeseries': time series for a set of indicators

If you just want a specific histogram, you can add a `histograms` parameter to the JSON header, specifying that histogram. For example:

    curl -H "Authorization: Bearer <your API token>" -H "Content-Type: application/json" -X POST -d '{"bibcodes":["1980ApJS...44..137K","1980ApJS...44..489B"],"types":["histograms"], "histograms":["publications"]}' https://api.adsabs.harvard.edu/v1/metrics

to get just the publications histogram. The service returns JSON with attributes determined by the contents of the `types` list (no such list means that everything gets returned). It always contains an attribute 'skipped bibcodes', which is a list of bibcodes for which no metrics data could be found. The following overview shows the JSON attributes returned by each type:

  * 'basic': 'basic stats' and 'basic stats refereed'
  * 'citations': 'citation stats' and 'citation stats refereed'
  * 'indicators': 'indicators' and 'indicators refereed'
  * 'histograms': 'histograms'
  * 'timeseries': 'time series'

Each of these attributes contains specific data elements. The following overview shows what each section contains (the phrases listed are the attribute names).

### 'basic stats' and 'basic stats refereed'
  * number of papers
  * normalized paper count
  * median number of reads
  * average number of reads
  * total number of reads
  * normalized number of reads
  * median number of downloads
  * average number of downloads
  * total number of downloads
  * normalized number of downloads

### 'citation stats' and 'citation stats refereed'
  * number of citing papers
  * median number of citations
  * average number of citations
  * total number of citations
  * normalized number of citations
  * median number of refereed citations
  * average number of refereed citations
  * total number of refereed citations
  * normalized number of refereed citations
  * number of self-citations

### 'indicators'
  * i10
  * i100
  * h
  * m
  * g
  * read10
  * tori

### 'histograms'
For all histograms, the actual histogram values are stored as follows:

    {
	    "histogram name": {year: value, year: value, ...}
	}

where values can be either integers or floats, depending on the type of histograms. The histogram name is an attribute of the histogram type. For example, the `publications` type has 4 separate histograms: `all publications`, `refereed publications`, `all publications normalized` and `refereed publications normalized`, which are organized as follows in the JSON output:

    {
	    "histograms":  {
			"publications": {
				"all publications": {},
				"refereed publications": {},
				"all publications normalized": {},
				"refereed publications normalized": {},
			
			}
		}
	}

The following overview lists for all histogram types the names of the actual histograms stored in them:

  * 'publications': 'all publications', 'refereed publications', 'all publications normalized', 'refereed publications normalized'
  * 'reads': 'all reads', 'refereed reads', 'all reads normalized', 'refereed reads normalized'
  * 'downloads': 'all downloads', 'refereed downloads', 'all downloads normalized', 'refereed downloads normalized'
  * 'citations': 'refereed to refereed', 'nonrefereed to refereed', 'refereed to nonrefereed', 'nonrefereed to nonrefereed', 'refereed to refereed normalized', 'nonrefereed to refereed normalized', 'refereed to nonrefereed normalized', 'nonrefereed to nonrefereed normalized'

Note that 'refereed reads' means: 'number of reads for the refereed publications in the set'.

### 'timeseries'
The `timeseries` attribute contains time series data for: `h`, `g`, `i10`, `i100`, `read10` and `tori`. The output is structured as

    {
		"time series": {
			"h": { values },
			"g": { values },
			"i10": { values },
			"i100": { values },
			"read10": { values },
			"tori": { values },
		
		}
	}

where the 'values' are organized in the same way as for the histograms: 

    {
	    "indicator name": {year: value, year: value, ...}
	}

## Everything together
So, returning everything, the output looks like

    {
		"skipped bibcodes": [ ... ],
		"basic stats":
		{
			"number of papers": 1,
			"normalized paper count": 0.1,
			"median number of reads": 1.1,
			"average number of reads": 1.1,
			"total number of reads": 1,
			"normalized number of reads": 0.1,
			"median number of downloads": 1.1,
			"average number of downloads": 1.1,
			"total number of downloads": 1,
			"normalized number of downloads": 0.1,			
			},
		"basic stats refereed":
		{
			"number of papers": 1,
			"normalized paper count": 0.1,
			"median number of reads": 1.1,
			"average number of reads": 1.1,
			"total number of reads": 1,
			"normalized number of reads": 0.1,
			"median number of downloads": 1.1,
			"average number of downloads": 1.1,
			"total number of downloads": 1,
			"normalized number of downloads": 0.1,			
			},
		"citation stats":
		{
			"number of citing papers": 1,
			"median number of citations": 0.1,
			"average number of citations": 1.1,
			"total number of citations": 1,
			"normalized number of citations": 0.1,
			"median number of refereed citations": 0.1,
			"average number of refereed citations": 1.1,
			"total number of refereed citations": 1,
			"normalized number of refereed citations": 0.1,	
			"number of self-citations": 1,		
			},
		"citations stats refereed":
		{
			"number of citing papers": 1,
			"median number of citations": 0.1,
			"average number of citations": 1.1,
			"total number of citations": 1,
			"normalized number of citations": 0.1,
			"median number of refereed citations": 0.1,
			"average number of refereed citations": 1.1,
			"total number of refereed citations": 1,
			"normalized number of refereed citations": 0.1,	
			"number of self-citations": 1,		
			},
		"indicators":
		{
			"i10": 1,
			"i100": 1,
			"h": 1,
			"m": 1.1,
			"g": 1,
			"read10": 0.1,
			"tori": 1.1,
			"riq": 1,	
			},
		"indicators refereed":
		{
			"i10": 1,
			"i100": 1,
			"h": 1,
			"m": 1.1,
			"g": 1,
			"read10": 0.1,
			"tori": 1.1,
			"riq": 1,
			},
		"histograms":
		{
			"publications": {
				"all publications": { values },
				"refereed publications": { values },
				"all publications normalized": { values },
				"refereed publications normalized": { values },
				},
			"reads": {
				"all reads": { values },
				"refereed reads": { values },
				"all reads normalized": { values },
				"refereed reads normalized": { values },
				},
			"downloads": {
				"all downloads": { values },
				"refereed downloads": { values },
				"all downloads normalized": { values },
				"refereed downloads normalized": { values },
				},
			"citations": {
				"refereed to refereed": { values },
				"nonrefereed to refereed": { values },
				"refereed to nonrefereed": { values },
				"nonrefereed to nonrefereed": { values },
				"refereed to refereed normalized": { values },
				"nonrefereed to refereed normalized": { values },
				"refereed to nonrefereed normalized": { values },
				"nonrefereed to nonrefereed normalized": { values },
				},
		},
		"time series":
		{
			"h": { values },
			"g": { values },
			"i10": { values },
			"i100": { values },
			"read10": { values },
			"tori": { values },
		}
	}

where, as before, the 'values' have the form

    {year: value, year: value, ...}
