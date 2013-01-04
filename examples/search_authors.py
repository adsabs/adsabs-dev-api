'''
This is an example script for a typical ADS use case: a simple
institutional bibliography. It accepts as input a file containing 
author names. It then searches ADS for records and outputs a tsv 
of bibcodes, titles, publication and full author list
'''

import sys
import simplejson
import requests

# base API search url
BASE_URL = 'http://adslabs.org/adsabs/api/search/'

# developer API access key
DEV_KEY = 'Dpn7HKuAlNos4Yhw'

for input in sys.argv[1:]:
    fp = open(input, 'rb')
    
    # for paginating through long results
    start = 0
    processed = 0
    
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
        
        while True:
            params['start'] = start
            r = requests.get(BASE_URL, params=params, headers=headers)
            sys.stderr.write(r.url + "\n")
            
            if r.status_code != requests.codes.ok:
                # hopefully if something went wrong you'll get a json error message
                e = simplejson.loads(r.text)
                sys.stderr.write("error retrieving results for author %s: %s\n" % (author, e['error']))
                continue

            data = simplejson.loads(r.text)
            hits = data['meta']['hits']
            processed += data['meta']['count']
            
            for d in data['results']['docs']:
                print d['bibcode'] + "\t" + d['title'] + "\t" + d['pub'] + "\t" + ';'.join(d['author'])
            sys.stderr.write("status: processed %d of %d results for author %s\n" % (processed, hits, author))
            
            if processed < hits:
                start = processed + 1
            else:
                break
