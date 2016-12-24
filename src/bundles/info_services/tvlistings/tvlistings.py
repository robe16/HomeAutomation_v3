from src.bundles.info_services.info_service import InfoService
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
                return str(self._listings)
        except Exception as e:
            print_error('Failed to return requested data {request} - {error}'.format(request=request['data'],
                                                                                     error=e))
            return False

    def _listings_process(self):
        #
        # TODO run once an hour (duration TBD) to remove times that have passed and add next 'batch' of listings
        while True:
            self.build_listing_dict()
            sleep(self._sleep_duration())

    def build_listing_dict(self):
        #
        data = read_list_channels()
        #
        for cat in data['channels']:
            _temp_chan = {}
            for chan in data['channels'][cat]['channels']:
                try:
                    _temp_chan[str(chan)] = self._getlisting(data['channels'][cat]['channels'][chan])
                except Exception as e:
                    print_error('Could not retrieve listings for {channel} - {error}'.format(channel=data['channels'][cat]['channels'][chan]['name'],
                                                                                             error=e))
                self._listings[str(cat)] = _temp_chan

    def _getlisting(self, data):
        #
        listing_srcs = data['listingsrc']
        #
        if not listing_srcs:
            print_msg('No sources available to retrieve listings for {channel}'.format(channel=data['name']))
            return {}
        #
        if len(listing_srcs)>0:
            for src, code in listing_srcs.items():
                try:
                    if src == 'bleb':
                        print_msg('TV listing for {channel} being retrieved from {src}'.format(channel=data['name'],
                                                                                                  src=src))
                        return data_source_bleb.get(code)
                except Exception as e:
                    print_error('TV listing for {channel} failed to be retrieved from {src} - {error}'.format(channel=data['name'],
                                                                                                              src=src,
                                                                                                              error=e))
        return {}

    def _sleep_duration(self):
        hour_to_cotinue = 6
        t = datetime.today()
        future = datetime(t.year, t.month, t.day, hour_to_cotinue, 0)
        if t.hour >= hour_to_cotinue:
            future += timedelta(days=1)
        return (future - t).seconds