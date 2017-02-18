from lists.bundles.list_bundles import get_bundle_detail
import requests


# http://datapoint.metoffice.gov.uk/public/data/

BASE_URL = 'https://newsapi.org/v1'
URI_ARTICLES = '/articles'
QUERY_ARTICLES_APIKEY = 'apiKey={api_key}'
QUERY_ARTICLES_SOURCE = 'source={source}'
QUERY_ARTICLES_SORTBY = 'sortBy={sortby}'
LIST_SORTBY = ['top', 'latest', 'popular']
URI_SOURCES = '/sources'
QUERY_SOURCES_CATEGORY = 'category={category}'
LIST_CATEGORY = ['business', 'entertainment', 'gaming', 'general', 'music', 'science-and-nature', 'sport', 'technology']
QUERY_SOURCES_LANGUAGE = 'language={language}'
LIST_LANGUAGE = ['en', 'de', 'fr']
QUERY_SOURCES_COUNTRY = 'country={country}'
LIST_COUNTRY = ['au', 'de', 'gb', 'in', 'it', 'us']


def get_articles(source='', sortby=''):
    #
    if source == '':
        raise Exception
    if sortby not in LIST_SORTBY:
        raise Exception
    #
    query = QUERY_ARTICLES_APIKEY.format(api_key=get_bundle_detail('newsapi', 'app_key'))
    query += '&' + QUERY_ARTICLES_SOURCE.format(source=source)
    if not sortby=='':
        query += '&' + QUERY_ARTICLES_SORTBY.format(sortby=sortby)
    #
    url = '{url}{uri}?{query}'.format(url=BASE_URL,
                                      uri=URI_ARTICLES,
                                      query=query)
    #
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return {'status': 'ERROR'}


def get_sources(category='', language='en', country=''):
    #
    if not category == '' and category not in LIST_CATEGORY:
        raise Exception
    if language not in LIST_LANGUAGE:
        raise Exception
    if not country == '' and country not in LIST_COUNTRY:
        raise Exception
    #
    if not category=='':
        query = QUERY_SOURCES_CATEGORY.format(category=category) + '&'
    else:
        query = ''
    #
    query += QUERY_SOURCES_LANGUAGE.format(language=language) + '&'
    query += QUERY_SOURCES_COUNTRY.format(country=country)
    #
    url = '{url}{uri}?{query}'.format(url=BASE_URL,
                                      uri=URI_SOURCES,
                                      query=query)
    #
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return {'status': 'ERROR'}

