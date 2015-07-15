from ConfigParser import ConfigParser
import dataholder
import os


def read_config():
    cfg = ConfigParser()
    if not cfg.read(os.path.join(os.path.dirname(__file__), "config.ini")):
        print 'Error: cannot load config.ini'
        return
    #
    dataholder.STRloungetv_lgtv_ipaddress = cfg.get('Lounge', 'LGTV_ipaddress')
    dataholder.STRloungetv_lgtv_pairkey = cfg.get('Lounge', 'LGTV_pairkey')
    dataholder.STRloungetv_tivo_ipaddress = cfg.get('Lounge', 'TIVO_ipaddress')
    dataholder.STRloungetv_tivo_mak = cfg.get('Lounge', 'TIVO_mak')
    dataholder.STRrocki_ipaddress = cfg.get('Kitchen', 'Rocki_ipaddress')
    dataholder.STRnest_pincode = cfg.get('Nest', 'Pincode')
    dataholder.STRnest_token = cfg.get('Nest', 'Token')
    dataholder.STRnest_tokenexp = cfg.get('Nest', 'Token_expiry')


def write_config():
    #
    cfg = ConfigParser()
    cfgfile = open("config.ini",'w')
    #
    cfg.add_section('Lounge')
    cfg.set('Lounge','LGTV_ipaddress',dataholder.STRloungetv_lgtv_ipaddress)
    cfg.set('Lounge','LGTV_pairkey', dataholder.STRloungetv_lgtv_pairkey)
    cfg.set('Lounge','TIVO_ipaddress', dataholder.STRloungetv_tivo_ipaddress)
    cfg.set('Lounge','TIVO_mak', dataholder.STRloungetv_tivo_mak)
    cfg.add_section('Kitchen')
    cfg.set('Kitchen','Rocki_ipaddress', dataholder.STRrocki_ipaddress)
    cfg.add_section('Nest')
    cfg.set('Nest','Pincode', dataholder.STRnest_pincode)
    cfg.set('Nest','Token', dataholder.STRnest_token)
    cfg.set('Nest','Token_expiry', dataholder.STRnest_tokenexp)
    #
    cfg.write(cfgfile)
    cfgfile.close()