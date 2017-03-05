# -*- coding: utf-8 -*-
import sys
import requests
import log

from bs4 import BeautifulSoup



#http://www.crmotos.com/clasificados/motos/search-results.html
#http://www.crmotos.com/clasificados/motos/search-results/index1.html
#http://www.crmotos.com/clasificados/motos/search-results/index94.html
CRMOTOS_URL = 'http://www.crmotos.com/clasificados/motos/search-results.html'
CRMOTOS_LISTING_PAGE_BASE = 'http://www.crmotos.com/clasificados/motos/search-results/index{}.html'

_crmotos_listings = set()

logger = log.setup_logger()

def get_request(url):
    logger.debug(url)
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        logger.exception('{} not found'.format(url))
        sys.exit(1)
    return r

def parse_page_counts(soup):
    '''Get the number of total pages with listings'''
    li_transit = soup.find('li', class_="transit")
    page_start, page_end = (li_transit.contents[2]['value']).split('|')
    return (int(page_start), int(page_end))

def parse_listing_urls(soup):
    '''Get the listings div, and all links in that div. Then get each 6th div.'''
    return [ l.attrs['href'] for l in  soup.find('div', id='listings').find_all('a')[::6] ]

def parse_details(soup, mapping):
    '''Get the details for the item'''
    return {v: trim_string(soup.find('tr', id=k).contents[3].contents[0]) for k, v in mapping.items()}

def trim_string(s):
    return s.strip(' \n\t')

def create_page_listing_urls(base_url, start, end):
    '''http://www.crmotos.com/clasificados/motos/search-results/index1.html'''
    return [base_url.format(i) for i in range(start, end+1)]

def store_listings(listings):
    _crmotos_listings.update(listings)

if __name__ == '__main__':

    r = get_request(CRMOTOS_URL)
    soup = BeautifulSoup(r.text, 'html.parser')

    page_start, page_end = parse_page_counts(soup)

    if(page_end < 2):
        sys.exit(1)

    #we know how many listings
    print(page_start, page_end)


    # get listing urls from first page
    listing_urls = parse_listing_urls(soup)
    store_listings(listing_urls)

    # now get the rest
    listing_pages = create_page_listing_urls(CRMOTOS_LISTING_PAGE_BASE, 2, page_end)

    for url in listing_pages:
        r = get_request(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        listing_urls = parse_listing_urls(soup)
        store_listings(listing_urls)

    #print(_crmotos_listings)

    detail_data_mapping = {'df_field_title': 'title',
                           'df_field_body_style': 'brand',
                           'df_field_moto_modelo': 'model',
                           'df_field_built': 'year',
                           'df_field_mileage': 'mileage',
                           'df_field_cubic_centimeters': 'cubic_centimeters',
                           'df_field_description_add': 'description',
                           'df_field_campo_telefono': 'phone',
                           'df_field_campo_celular': 'cell',
                           'df_field_city': 'city',
                           'df_field_b_states': 'state'
                           }

    # now, for each listing, get the details about the item
    for url in _crmotos_listings:

        r = get_request(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        details = soup.find("td", class_="details")

        detail_data = parse_details(details, detail_data_mapping)

        print(detail_data)
        exit()














