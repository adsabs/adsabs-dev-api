'''
This is an example script that illustrates the usefulness of 
faceted search output. Like the search_authors.py script it
accepts as input a file containing author names. It then searches ADS for 
matching records, but retrieves stats about those authors via
article property and publication facet data. We'll then output
each author along with his/her could of referreed vs. non-refereed 
articles and his/her top-3 publication venues
'''

import os
import sys
import simplejson
import requests

# base API search url
BASE_URL = 'http://adslabs.org/adsabs/api/search/'

# developer API access key
DEV_KEY = ''

if os.environ.has_key("ADS_DEV_KEY"):
    DEV_KEY = os.environ['ADS_DEV_KEY']

for input in sys.argv[1:]:
    fp = open(input, 'rb')
    
    for line in fp:
        author = line.strip()
        params = {}
        
        # basic author search
        params['q'] = "author:%s" % author
        
        # we're not interested in the acutal result documents
        params['rows'] = '0'
        
        # the 'facet' param is repeatable so we can pass a list of values to the request
        # here we indicate we want facet data for the 'property' and 'bibstem' fields
        # for the bibstem field we set a 'limit' of 3 since we only want the top three values
        params['facet'] = ['property', 'bibstem:3']
        
        # include our access key
        params['dev_key'] = DEV_KEY
        
        # json is the default type, this is just for illustration purposes
        headers = {'content-type': 'application/json'}
        
        sys.stderr.write("issuing query for author %s\n" % author)
        
        r = requests.get(BASE_URL, params=params, headers=headers)
        sys.stderr.write(r.url + "\n")
        
        if r.status_code != requests.codes.ok:
            # hopefully if something went wrong you'll get a json error message
            e = simplejson.loads(r.text)
            sys.stderr.write("error retrieving results for author %s: %s\n" % (author, e['error']))
            continue

        data = simplejson.loads(r.text)
        
        # turn property facet data into a dict
        properties_data = data['results']['facets']['facet_fields']['property']
        properties = dict([tuple(properties_data[i:i+2]) for i in xrange(0, len(properties_data), 2)])
        
        # get top 3 most frequently appearing publication
        bibstem_data = data['results']['facets']['facet_fields']['bibstem']
        top_pubs = ["%s:%d" % tuple(bibstem_data[i:i+2]) for i in xrange(0, len(bibstem_data), 2)]
        
        # output author \t refereed count \t non-refereed count \t top publications
        print "%s\t%d\t%d\t%s" % (author, properties['refereed'], properties['notrefereed'], ','.join(top_pubs))
        
