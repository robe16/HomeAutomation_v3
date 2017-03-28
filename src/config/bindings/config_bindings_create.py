from bindings.tv_lg_netcast.tv_lg_netcast import device_tv_lg_netcast
from bindings.tivo.tivo import device_tivo
from bindings.nest.nest import account_nest
from bindings.news.news import info_news
from bindings.weather.weather import info_metoffice
from bindings.tvlistings.tvlistings import info_tvlistings

from config.bindings.config_bindings import get_cfg_bindings_json
from config.bindings.config_bindings import get_cfg_thing_type
from log.console_messages import print_msg, print_error


def create_bindings(_things):
    #
    data = get_cfg_bindings_json()
    #
    group_seq = 0
    for group in data['bindings']['groups']:
        #
        _things[group_seq] = {}
        group_things = {}
        #
        thing_seq = 0
        for thing in group['things']:
            #
            try:
                group_things[thing_seq] = _create_thing(thing['type'], group_seq, thing_seq)
                print_msg('Thing created: {type}: {group}:{thing}'.format(type=thing['type'],
                                                                           group=group['name'],
                                                                           thing=thing['name']))
            except Exception as e:
                print_error('Coud not create Thing: {type}: {group}:{thing}'.format(type=thing['type'],
                                                                                    group=group['name'],
                                                                                    thing=thing['name']))
            #
            thing_seq += 1
        #
        _things[group_seq] = group_things
        #
        group_seq += 1
    #
    print_msg('All devices and infoservice instances created')


def _create_thing(thing_type, group_seq, thing_seq):
    #
    if thing_type=='tv_lg_netcast':
        return device_tv_lg_netcast(group_seq, thing_seq)
    elif thing_type=='tivo':
        return device_tivo(group_seq, thing_seq)
    elif thing_type=='nest_account':
        return account_nest(group_seq, thing_seq)
    elif thing_type=='weather':
        return info_metoffice(group_seq, thing_seq)
    elif thing_type=='tvlistings':
        return info_tvlistings(group_seq, thing_seq)
    elif thing_type=='news':
        return info_news(group_seq, thing_seq)
    else:
        return False