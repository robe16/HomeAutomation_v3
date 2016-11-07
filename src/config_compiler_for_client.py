from config_devices import get_cfg_device_json
import ast

def compile_config():
    #
    cfg = get_cfg_device_json()
    #
    for s in cfg['structures']:
        #
        for a in cfg['structures'][s]['accounts']:
            del cfg['structures'][s]['accounts'][a]['details']
            #
        for r in cfg['structures'][s]['rooms']:
            for d in cfg['structures'][s]['rooms'][r]['devices']:
                del cfg['structures'][s]['rooms'][r]['devices'][d]['details']
                #
    #
    try:
        return ast.literal_eval(cfg)
    except:
        return cfg