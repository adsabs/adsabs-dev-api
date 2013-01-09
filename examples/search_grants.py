'''
This is an example script for a typical ADS use case. It accepts 
as input a file containing NASA grant ids. It then searches ADS 
for records matching those ids and outputs a tsv of bibcodes 
mapped to the grant ids they contain
'''

import os
import sys
import simplejson
import requests

# base API search url
BASE_URL = 'http://adslabs.org/adsabs/api/search/'

# base query for use as a "filter" query
FILTER_QUERY = '(NASA OR "National Aeronautics and Space Administration") AND grant'

# developer API access key
DEV_KEY = ''

if os.environ.has_key("ADS_DEV_KEY"):
    DEV_KEY = os.environ['ADS_DEV_KEY']

for input in sys.argv[1:]:
    fp = open(input, 'rb')

    for line in fp:
        org, grant = line.strip().split()
        params = {}
        
        # use the actual grant identifier as a primary query
        params['q'] = grant
        
        # sending this part of the query as a "filter" has two benefits
        #  - the search engine is able to cache and re-use the results of the filter independently
        #  - separating out the non-changing parts of the query can make complex queries easier to compose
        params['filter'] = FILTER_QUERY
        
        # we only want to get the ADS bibcodes back in the response
        params['fl'] = 'bibcode'
        
        # include our access key
        params['dev_key'] = DEV_KEY
        
        # json is the default type, this is just for illustration purposes
        headers = {'content-type': 'application/json'}
        
        sys.stderr.write("issuing query for grant %s\n" % grant)
        r = requests.get(BASE_URL, params=params, headers=headers)
        
        # uncomment if you want to see the actual http request url
        #sys.stderr.write(r.url + "\n")
            
        if r.status_code != requests.codes.ok:
            # hopefully if something went wrong you'll get a json error message
            e = simplejson.loads(r.text)
            sys.stderr.write("error retrieving results for grant %s: %s\n" % (grant, e['error']))
            continue

        data = simplejson.loads(r.text)
        hits = data['meta']['hits']
        sys.stderr.write("found %d document for grant %s\n" % (hits, grant))
        
        for d in data['results']['docs']:
            print d['bibcode'] + "\t" + org + "\t" + grant
