'''
This is an example script for a typical ADS use case: a simple
institutional bibliography. It accepts as input a file containing 
author names. It then searches ADS for records and outputs a tsv 
of bibcodes, titles, publication and full author list
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
        
        # the fields we want back
        params['fl'] = 'bibcode,title,pub,author'
        
        # process 100 results at a time
        params['rows'] = '100'
        
        # include our access key
        params['dev_key'] = DEV_KEY
        
        # json is the default type, this is just for illustration purposes
        headers = {'content-type': 'application/json'}
        
        sys.stderr.write("issuing query for author %s\n" % author)
        
        # for paginating through long results
        start = 0
        processed = 0
        
        while True:
            params['start'] = start
            r = requests.get(BASE_URL, params=params, headers=headers)
            
            # uncomment if you want to see the actual http request url
            # sys.stderr.write(r.url + "\n")
            
            if r.status_code != requests.codes.ok:
                # hopefully if something went wrong you'll get a json error message
                e = simplejson.loads(r.text)
                sys.stderr.write("error retrieving results for author %s: %s\n" % (author, e['error']))
                continue

            data = simplejson.loads(r.text.decode('utf-8'))
            hits = data['meta']['hits']
            count = data['meta']['count']
            processed += count
            
            for d in data['results']['docs']:
#                author_list = [x.encode('utf-8') for x in d['author']]
#                title = d['title'].encode('utf-8')
#                print d['bibcode'] + "\t" + title + "\t" + d.get('pub', '') + "\t" + ';'.join(author_list)
                out = d['bibcode'] + "\t" + d['title'] + "\t" + d.get('pub', '') + "\t" + ';'.join(d['author'])
                print out.encode('utf-8')
            sys.stderr.write("status: processed %d of %d results for author %s\n" % (processed, hits, author))
            
            if processed < hits:
                start += count
            else:
                break
