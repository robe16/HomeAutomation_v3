import time
from urllib import urlopen

import src.cfg as cfg
from src.config.devices.config_devices import get_cfg_device_detail
from src.lists.devices.list_devices import get_device_detail, get_device_name, get_device_logo, get_device_html_command, get_device_html_settings
from src.log.console_messages import print_msg


class Device:

    def __init__(self, type, room_id, device_id, q_dvc, queues):
        #
        self._active = True
        #
        self._type = type
        self._room_id = room_id
        self._device_id = device_id
        #
        self._queue = q_dvc
        self._q_response_data = queues[cfg.key_q_response_data]
        self._q_response_cmd = queues[cfg.key_q_response_command]
        self._q_tvlistings = queues[cfg.key_q_tvlistings]

    def dvc_or_acc_id(self):
        return self._room_id + ':' + self._device_id

    def dvc_or_acc_ref(self):
        return self._room_id + '_' + self._device_id

    def _ipaddress(self):
        return get_cfg_device_detail(self._room_id, self._device_id, "ipaddress")

    def _port(self):
        return get_device_detail(self._type, "port")

    def _logo(self):
        return get_device_logo(self._type)

    def _dvc_name(self):
        return get_cfg_device_detail(self._room_id, self._device_id, "name")

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
            '''
                Use of self._active allows for object to close itself, however may wish
                to take different approach of terminating the thread the object loop resides in
            '''
            time.sleep(0.1)
            qItem = self._getFromQueue()
            if bool(qItem):
                if qItem['response_queue'] == 'stop':
                    self._active = False
                elif qItem['response_queue'] == cfg.key_q_response_data:
                    self._q_response_data.put(self.getData(qItem['request']))
                elif qItem['response_queue'] == cfg.key_q_response_command:
                    self._q_response_cmd.put(self.sendCmd(qItem['request']))
                else:
                    # Code to go here to handle other items added to the queue!!
                    True
        print_msg('Thread stopped: {type}'.format(type=self._type), dvc_or_acc_id=self.dvc_or_acc_id())

    def sendCmd(self, request):
        # Mastered in each of the device specific classes
        True

    def getData(self, request):
        # Mastered in each of the device specific classes
        True

    def _getHtml_generic(self, args):
        return urlopen('web/html/html_devices/' + get_device_html_command(self._type)).read().encode('utf-8').format(**args)

    def getHtml_settings(self, room_num, dvc_num):
        # Mastered in each of the device specific classes
        True

    def getHtml_settings_generic(self, args):
        html_file = get_device_html_settings(self._type)
        if html_file:
            return urlopen('web/html/html_devices/' + html_file).read().encode('utf-8').format(**args)
        else:
            return ''