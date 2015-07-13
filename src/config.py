import ConfigParser

def write_config(lounge_tv_ip, lounge_tv_pair,
                 lounge_tivo_ip, lounge_tivo_mak,
                 kitchen_rocki_ip,
                 nest_ip, nest_token, nest_tokenexp):
    #
    Config = ConfigParser.ConfigParser()
    cfgfile = open("config.ini",'w')
    #
    Config.add_section('Lounge')
    Config.set('Lounge','LGTV_ipaddress',lounge_tv_ip)
    Config.set('Lounge','LGTV_pairkey', lounge_tv_pair)
    Config.set('Lounge','TIVO_ipaddress', lounge_tivo_ip)
    Config.set('Lounge','TIVO_mak', lounge_tivo_mak)
    Config.add_section('Kitchen')
    Config.set('Kitchen','Rocki_ipaddress', kitchen_rocki_ip)
    Config.add_section('Nest')
    Config.set('Nest','Pincode', nest_ip)
    Config.set('Nest','Token', nest_token)
    Config.set('Nest','Token_expiry', nest_tokenexp)
    #
    Config.write(cfgfile)
    cfgfile.close()

