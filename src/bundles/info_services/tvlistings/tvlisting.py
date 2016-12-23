from datetime import datetime

import data_source_radiotimes
import data_source_bleb
from src.lists.channels.list_channels import read_list_channels, get_channel_item_listingsrc_all
from src.log.console_messages import print_msg


def build_listing_dict():
    #
    listing_dict = {}
    #
    data = read_list_channels()
    #
    for cat in data['channels']:
        listing_dict[cat] = {}
        for chan in data['channels'][cat]['channels']:

            listing_dict[cat][chan] = _getlisting(cat, chan)
    #
    return listing_dict


def _getlisting(cat, chan):
    #
    src = get_channel_item_listingsrc_all(cat, chan)
    #
    if len(src)>0:
        for src, code in src:
            try:
                if src == 'bleb':
                    return data_source_bleb.get(code)
            except:
                pass
            # Code for radiotimes 'muted' due to decommision of radiotimes API
            # try:
            #     if src == 'radiotimes':
            #         return data_source_radiotimes.getlisting(code)
            # except:
            #     pass
    print_msg('No known listing source available')
    return False
