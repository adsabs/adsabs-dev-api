'''
This is an example script for a typical ADS use case. It accepts 
as input a file containing NASA grant ids. It then searches ADS 
for records matching those ids and outputs a tsv of bibcodes 
mapped to the grant ids they contain
'''

import sys
import simplejson
import httplib2
from urllib import urlencode

# base API search url
BASE_URL = 'http://adslabs.org/adsabs/api/search/?'

# base query to which we append each grant id
BASE_QUERY = '(NASA OR "National Aeronautics and Space Administration") AND grant AND %s'

# developer API access key
DEV_KEY = ''

h = httplib2.Http(".cache")

for input in sys.argv[1:]:
    fp = open(input, 'rb')

    for line in fp:
        org, grant = line.strip().split()
        query = BASE_QUERY % grant
        params = {
            'q': query,
            'fl': 'bibcode',
            'dev_key': DEV_KEY,
            }
        
        url = BASE_URL + urlencode(params)
        sys.stderr.write("issuing query for grant %s: %s\n" % (grant, url))
        resp, content = h.request(url, "GET")
        
        if resp.status != 200:
            sys.stderr.write("error retrieving results for grant %s\n" % grant)

        data = simplejson.loads(content)
        hits = data['meta']['hits']
        sys.stderr.write("found %d document for grant %s\n" % (hits, grant))
        
        for d in data['results']['docs']:
            print d['bibcode'] + "\t" + grant
