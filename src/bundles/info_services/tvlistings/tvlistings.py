from src.bundles.info_services.info_service import InfoService
# import data_source_radiotimes
import data_source_bleb
from src.lists.channels.list_channels import read_list_channels, get_channel_item_listingsrc_all
from src.log.console_messages import print_msg, print_error
from multiprocessing import Process, Manager
from datetime import datetime, timedelta
from time import sleep


class info_tvlistings(InfoService):

    _listings = Manager().dict()

    def __init__ (self):
        #
        InfoService.__init__(self, 'tvlistings')
        #
        Process(target=self._listings_process).start()

    def getData(self, request):
        try:
            if request['data'] == 'alllistings':
                return self._listings
        except Exception as e:
            print_error('Failed to return requested data {request} - {error}'.format(request=request['data'],
                                                                                     error=e))
            return False

    def _listings_process(self):
        #
        while True:
            self._listings = self.build_listing_dict()
            sleep(self._sleep_duration())

    def build_listing_dict(self):
        #
        listing_dict = {}
        #
        data = read_list_channels()
        #
        for cat in data['channels']:
            listing_dict[cat] = {}
            for chan in data['channels'][cat]['channels']:
                listing_dict[cat][chan] = self._getlisting(cat, chan)
        #
        return listing_dict

    def _getlisting(self, cat, chan):
        #
        listing_srcs = get_channel_item_listingsrc_all(cat, chan)
        #
        if not listing_srcs:
            print_msg('No sources available to retrieve listings for {cat}.{chan}'.format(cat=cat,
                                                                                          chan=chan))
            return False
        #
        if len(listing_srcs)>0:
            for src, code in listing_srcs.items():
                try:
                    if src == 'bleb':
                        listing = data_source_bleb.get(code)
                        print_msg('TV listings retrieved from {src} for {cat}.{chan}'.format(src=src,
                                                                                             cat=cat,
                                                                                             chan=chan))
                        return listing
                except:
                    pass
                # Code for radiotimes 'muted' due to decommision of radiotimes API
                # try:
                #     if src == 'radiotimes':
                #         return data_source_radiotimes.getlisting(code)
                # except:
                #     pass
        return False

    def _sleep_duration(self):
        t = datetime.today()
        future = datetime(t.year, t.month, t.day, 6, 0)
        if t.hour >= 2:
            future += timedelta(days=1)
        return (future - t).seconds