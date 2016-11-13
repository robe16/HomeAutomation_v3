import time
from urllib import urlopen
import src.cfg as cfg
from src.config.devices.config_devices import get_cfg_account_detail
from src.lists.devices.list_devices import get_device_detail, get_device_name, get_device_logo, get_device_html_command, get_device_html_settings
from src.console_messages import print_command, print_error, print_msg


class Account:

    def __init__(self, type, account_id, q_dvc, queues):
        #
        self._active = True
        #
        self._type = type
        self._account_id = account_id
        #
        self._queue = q_dvc
        self._q_response_web = queues[cfg.key_q_response_web_device]
        self._q_response_cmd = queues[cfg.key_q_response_command]
        self._q_tvlistings = queues[cfg.key_q_tvlistings]

    def dvc_or_acc_id(self):
        return self._account_id

    def dvc_or_acc_ref(self):
        return self._account_id

    def _logo(self):
        return get_device_logo(self._type)

    def _dvc_name(self):
        return get_cfg_account_detail(self._account_id, "name")

    def _type_name(self):
        return get_device_name(self._type)

    def _getFromQueue(self):
        if not self._queue.empty():
            return self._queue.get(block=True)
        else:
            return False


    def run(self):
        time.sleep(5)
        while self._active:
            # Keep in a loop
            time.sleep(0.1)
            qItem = self._getFromQueue()
            if bool(qItem):
                if qItem['response_queue'] == 'stop':
                    self._active = False
                elif qItem['response_queue'] == cfg.key_q_response_web_device:
                    self._q_response_web.put(self.getHtml(user=qItem['user']))
                elif qItem['response_queue'] == cfg.key_q_response_command:
                    self._q_response_cmd.put(self.sendCmd(qItem['request']))
                else:
                    # Code to go here to handle other items added to the queue!!
                    True
        print_msg('Thread stopped: {type}'.format(type=self._type), dvc_or_acc_id=self.dvc_or_acc_id())

    def sendCmd(self, request):
        # Mastered in each of the device specific classes
        True

    def getHtml(self, user):
        # Mastered in each of the device specific classes
        True

    def _getHtml_generic(self, args):
        return urlopen('web/html_devices/' + get_device_html_command(self._type)).read().encode('utf-8').format(**args)

    def getHtml_settings(self, room_num, dvc_num):
        # Mastered in each of the device specific classes
        True

    def getHtml_settings_generic(self, args):
        html_file = get_device_html_settings(self._type)
        if html_file:
            return urlopen('web/html_devices/' + html_file).read().encode('utf-8').format(**args)
        else:
            return ''