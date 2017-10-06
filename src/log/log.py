from datetime import datetime
import logging
import os

# Logging Level Values:
#  CRITICAL 50
#  ERROR    40
#  WARNING  30
#  INFO     20
#  DEBUG    10
#  UNSET     0

logfile = os.path.join(os.path.dirname(__file__), 'server.log')
logging.basicConfig(filename=logfile, level=20)

timeformat = '%d/%m/%Y %H:%M:%S.%f'


def log_command(command, dvc_id, device_type, dvc_ip, response):
    log_msg = _add_timestamp("{dvc_id} - \'{command}\' request sent to {device_type}{dvc_ip} - {response}".format(dvc_id=dvc_id,
                                                                                                                  command=command.replace('/r',''),
                                                                                                                  device_type=device_type,
                                                                                                                  dvc_ip=' '+dvc_ip,
                                                                                                                  response=response))
    if "ERROR" in log_msg:
        logging.info(log_msg)
    else:
        logging.error(log_msg)


def log_error(error_msg, dvc_id=''):
    if (dvc_id):
        dvc_id += ' - '
    log_msg = _add_timestamp('{dvc_id}ERROR: {error}'.format(dvc_id=dvc_id,
                                                             error = error_msg))
    logging.error(log_msg)


def log_general(msg, dvc_id=''):
    if (dvc_id):
        dvc_id += ' - '
    log_msg = _add_timestamp('{dvc_id}{msg}'.format(dvc_id=dvc_id,
                                                    msg=msg))
    logging.info(log_msg)


def _add_timestamp(log_msg):
    return '{timestamp} - {log_msg}'.format(timestamp=datetime.now().strftime(timeformat),
                                            log_msg=log_msg)
