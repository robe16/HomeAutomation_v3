from bindings.info_services.info_service import InfoService
from log.console_messages import print_error
import json
from data_source_newsapi_org import get_articles, get_sources

CONFIG_LIST_SOURCES = []

class info_news(InfoService):

    def __init__ (self):
        #
        InfoService.__init__(self, 'news')

    def getData(self, request):
        try:
            if request['data'] == 'articles':
                return json.dumps(self.getNews(request['sources'].split(' '), request['sortby']))
        except Exception as e:
            print_error('Failed to return requested data {request} - {error}'.format(request=request['data'],
                                                                                     error=e))
            return False

    def getNews(self, request_sources, sortby):
        #
        sortby = str(sortby)
        #
        sources_details = get_sources()
        news = {'news_articles': {}}
        #
        for request_src in request_sources:
            #
            request_src = str(request_src)
            #
            src_details = {'name': '',
                           'description': '',
                           'url': '',
                           'category': '',
                           'logos': {'small': '',
                                     'medium': '',
                                     'large': ''}}
            #
            try:
                if sources_details['status'] == 'ok':
                    #
                    for src_detail_item in sources_details['sources']:
                        if str(src_detail_item['id']) == request_src:
                            #
                            # if the requested sortby is not available for the source,
                            # default to first in list for the source
                            if not sortby in src_detail_item['sortBysAvailable']:
                                sortby = src_detail_item['sortBysAvailable'][0]
                            #
                            src_details = {'name': src_detail_item['name'],
                                           'description': src_detail_item['description'],
                                           'url': src_detail_item['url'],
                                           'category': src_detail_item['category'],
                                           'logos': {'small': src_detail_item['urlsToLogos']['small'],
                                                     'medium': src_detail_item['urlsToLogos']['medium'],
                                                     'large': src_detail_item['urlsToLogos']['large']}}
                            break
            except Exception as e:
                pass
            #
            try:
                tmp_articles = get_articles(request_src, sortby)
                #
                if tmp_articles['status'] == 'ok':
                    #
                    news['news_articles'][request_src] = {}
                    news['news_articles'][request_src]['source_details'] = src_details
                    news['news_articles'][request_src]['articles'] = tmp_articles['articles']
            except Exception as e:
                print_error('Unable to retrieve news articles from newsapi.org - {source}:{sortby}'.format(source=request_src,
                                                                                                           sortby=sortby))
            #
        #
        return news
