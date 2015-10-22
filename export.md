## Export service

```
https://api.adsabs.harvard.edu/v1/export/:format
```
Currently, our API supports export in the following formats: AASTeX, BibTeX and EndNote. To get e.g. BibTeX for a set of records you do a POST request to the endpoint

    https://api.adsabs.harvard.edu/v1/export/bibtex

with in the POST header 

    {"bibcode":["<bibcode1>","<bibcode2>", ...]}
	
Using `curl`, to get the BibTeX for e.g. the record with bibcode `2015ApJS..219...21Z`, you would do

    curl -H "Authorization: Bearer <your API token>" -H "Content-Type: application/json" -X POST -d '{"bibcode":["2015ApJS..219...21Z"]}' https://api.adsabs.harvard.edu/v1/export/bibtex

and the API then responds in JSON with 

    {u'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', u'export': u'@ARTICLE{2015ApJS..219...21Z,\n   author = {{Zhang}, M. and {Fang}, M. and {Wang}, H. and {Sun}, J. and \n\t{Wang}, M. and {Jiang}, Z. and {Anathipindika}, S.},\n    title = "{A Deep Near-infrared Survey toward the Aquila Molecular Cloud. I. Molecular Hydrogen Outflows}",\n  journal = {\\apjs},\narchivePrefix = "arXiv",\n   eprint = {1506.08372},\n primaryClass = "astro-ph.SR",\n keywords = {infrared: ISM, ISM: jets and outflows, shock waves, stars: formation, stars: winds, outflows},\n     year = 2015,\n    month = aug,\n   volume = 219,\n      eid = {21},\n    pages = {21},\n      doi = {10.1088/0067-0049/219/2/21},\n   adsurl = {http://adsabs.harvard.edu/abs/2015ApJS..219...21Z},\n  adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'}

The get AASTeX back, you use `aastex` as format parameter, and `endnote` for EndNote.
