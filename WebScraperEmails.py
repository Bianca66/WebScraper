import re
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# starting_url = 'http://www.miet.ac.in'

class scrape_email:
    def scrape(self, url, nr_pages, file_name, path_file, format):
        ############# CRAWLING URL ###############
        starting_url = url
        ### Create a queue of urls to be crawled
        unprocessed_urls = deque([starting_url])
        ### Set of already crawled urls for email
        processed_urls = set()
        ### Create a list of list to store each e-mail
        table = []
        table.append([])
        ### Create a set of fetched emails
        emails = set()
        k = 0
        table[0].append("Links")
        table[0].append("E-mails ->")
        ### Process urls until queues is empty
        if nr_pages:
            a = nr_pages
            i = 1
        else:
            a = 1
            i = 0

        while len(unprocessed_urls) and not(a == 0):
            ### Next URL
            url = unprocessed_urls.popleft()
            processed_urls.add(url)

            ### Extract base url to resolve relative links
            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url
            # get url's content
            print("Crawling URL {}".format(url))
            k = k + 1
            table.append([])
            table[k].append(url)

            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.URLRequired):
                ### Ignore pages with errors and continue with next url
                continue

            ### Extract all email addresses and add them into the resulting set
            ### Create a pattern for regular expression
            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
            emails.update(new_emails)
            email = list(new_emails)

            for em in email:
                table[k].append(em)
            time.sleep(0.3)

            ### Create a beautiful soup object
            soup = BeautifulSoup(response.text, 'lxml')

            ### Find and process all the anchors i.e. linked urls in this document
            for anchor in soup.find_all("a"):
                ### Extract link url from the anchor
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                ### Resolve relative links (starting with /)
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                ### Add the new url to the queue if it was not in unprocessed list nor in processed list yet
                if not link in unprocessed_urls and not link in processed_urls:
                    unprocessed_urls.append(link)
            a = a - i

        s1 = pd.DataFrame(table)
        if format == 'CSV':
            s1.to_csv(os.path.join(path_file, '{}.csv'.format(file_name)), index=False)
        elif format == 'JSON':
            s1.to_json(os.path.join(path_file, '{}.json'.format(file_name)), index=True)
        else:
            s1.to_sql(os.path.join(path_file, '{}.json'.format(file_name)), index=True)
        print(s1)
        print(k)

#scrape_email.scrape(self=scrape_email,url='https://upb.ro/', nr_pages=20, file_name="Lala", path_file="/home/palade/Documents/proiecte/Sisteme de Operare", format="CSV")