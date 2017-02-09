#!/usr/bin/python 

import json
import logging
import random
import subprocess
import time
import urllib2

def main():
    logging.getLogger().setLevel(logging.INFO)
    while True:
        try:
            nearest_data = json.load(
                urllib2.urlopen('https://mlab-ns.appspot.com/ndt'))
            logging.info('Testing to %s', nearest_data['fqdn'])
            subprocess.check_call(['/ndt/src/web100clt', '--name', nearest_data['fqdn']])
            all_sites = json.load(
                urllib2.urlopen('https://mlab-ns.appspot.com/ndt?policy=all'))
            us_sites = [site for site in all_sites if site['country'] == 'US']
            us_site = random.choice(us_sites)
            logging.info('Testing to %s', us_site['fqdn'])
            subprocess.check_call(['/ndt/src/web100clt', '--name', us_site['fqdn']])
        except urllib2.URLError as ue:
            logging.error('Failed to access MLabNS: %s', ue.message)
        except subprocess.CalledProcessError as cpe:
            logging.error('Non-zero exit status: %d "%s"', cpe.returncode,
                          cpe.message)
        sleeptime = random.expovariate(1.0/3600.0)
        logging.info('About to sleep for %g seconds', sleeptime)
        time.sleep(sleeptime)

if __name__ == '__main__':
    main()
