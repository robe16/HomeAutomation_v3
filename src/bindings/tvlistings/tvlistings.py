import json
from datetime import datetime, timedelta
from multiprocessing import Process, Manager
from time import sleep

from bindings.info_service import InfoService
from lists.channels.list_channels import read_list_channels
from log.log import log_error, log_warning, log_general

import data_source_bleb


class info_tvlistings(InfoService):

    _listings = Manager().dict()

    def __init__ (self, info_seq):
        #
        InfoService.__init__(self, 'tvlistings', info_seq)
        #
        Process(target=self._listings_process).start()

    def getData(self, request):
        try:
            if request['data'] == 'alllistings':
                return json.dumps(self._listings.copy())
        except Exception as e:
            log_error('Failed to return requested data {request} - {error}'.format(request=request['data'],
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
                    log_error('Could not retrieve listings for {channel} - {error}'.format(channel=data['channels'][cat]['channels'][chan]['name'],
                                                                                           error=e))
                self._listings[str(cat)] = _temp_chan

    def _getlisting(self, data):
        #
        listing_srcs = data['listingsrc']
        #
        if not listing_srcs:
            log_warning('No sources available to retrieve listings for {channel}'.format(channel=data['name']))
            return {}
        #
        if len(listing_srcs)>0:
            for src, code in listing_srcs.items():
                try:
                    if src == 'bleb':
                        log_general('TV listing for {channel} being retrieved from {src}'.format(channel=data['name'],
                                                                                                  src=src))
                        return data_source_bleb.get(code)
                except Exception as e:
                    log_error('TV listing for {channel} failed to be retrieved from {src} - {error}'.format(channel=data['name'],
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