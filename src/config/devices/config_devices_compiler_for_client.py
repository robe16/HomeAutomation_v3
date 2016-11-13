import ast

from src.config.devices.config_devices import get_cfg_device_json


def compile_config():
    #
    cfg = get_cfg_device_json()
    #
    for s in cfg['structures']:
        #
        for a in cfg['structure']['accounts']:
            del cfg['structure']['accounts'][a]['details']
            #
        for r in cfg['structure']['rooms']:
            for d in cfg['structure']['rooms'][r]['devices']:
                del cfg['structure']['rooms'][r]['devices'][d]['details']
                #
    #
    try:
        return ast.literal_eval(cfg)
    except:
        return cfg