import platform
from math import fabs
from kivy.clock import Clock
import json
from paho.mqtt.client import Client
from lamp_common import *
import lampi_util
from IPython import embed

MQTT_CLIENT_ID = "sphinx_daemon"

class SphinxApp:
    _updated = False
    _hue = 0.0
    _saturation = 0.0
    _brightness = 0.0
    lamp_is_on = 0

    #def _get_hue(self):        return self._hue
    #def _set_hue(self, value): self._hue = value

    #def _get_saturation(self):        return self._saturation
    #def _set_saturation(self, value): self._saturation = value

    #def _get_brightness(self):        return self._brightness
    #def _set_brightness(self, value): self._brightness = value

    hue = 0 # AliasProperty(_get_hue, _set_hue, bind=['_hue'])
    saturation = 0 # AliasProperty(_get_saturation, _set_saturation, bind=['_saturation'])
    brightness = 0 # AliasProperty(_get_brightness, _set_brightness, bind=['_brightness'])
    gpio17_pressed = 0 # BooleanProperty(False)
    device_associated = 0 # BooleanProperty(True)

    def on_start(self):
        self._publish_clock = None
        self.mqtt_broker_bridged = False
        self._associated = True
        self.association_code = None
        self.mqtt = Client(client_id=MQTT_CLIENT_ID)
        self.mqtt.enable_logger()
        self.mqtt.will_set(client_state_topic(MQTT_CLIENT_ID), "0", qos=2, retain=True)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT, keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
        print("broker host", MQTT_BROKER_HOST, " mqtt broker port", MQTT_BROKER_PORT)
        #self.mqtt.loop_forever() #
        self.mqtt.loop_start()
        #self.set_up_GPIO_and_network_status_popup()
        #self.associated_status_popup = self._build_associated_status_popup()
        #self.associated_status_popup.bind(on_open=self.update_popup_associated)
        Clock.schedule_interval(self._poll_associated, 0.1)
        print("hue", self._hue, self.hue)
        print("saturation", self._saturation, self.saturation)
        print("brightness", self._brightness, self.brightness)
        print("onoff", self.lamp_is_on, Clock)

    def _build_associated_status_popup(self):
        return Popup(title='Associate your Lamp',
                     content=Label(text='Msg here', font_size='30sp'),
                     size_hint=(1, 1), auto_dismiss=False)

    def on_hue(self, instance, value):
        if self._updatingUI:
            return
        if self._publish_clock is None:
            self._publish_clock = Clock.schedule_once(
                lambda dt: self._update_leds(), 0.01)

    def on_saturation(self, instance, value):
        if self._updatingUI:
            return
        if self._publish_clock is None:
            self._publish_clock = Clock.schedule_once(
                lambda dt: self._update_leds(), 0.01)

    def on_brightness(self, instance, value):
        if self._updatingUI:
            return
        if self._publish_clock is None:
            self._publish_clock = Clock.schedule_once(
                lambda dt: self._update_leds(), 0.01)

    def on_lamp_is_on(self, instance, value):
        if self._updatingUI:
            return
        if self._publish_clock is None:
            self._publish_clock = Clock.schedule_once(
                lambda dt: self._update_leds(), 0.01)

    def on_connect(self, client, userdata, flags, rc):
        print("lampi_sphinx_app on_connect")
        self.mqtt.publish(client_state_topic(MQTT_CLIENT_ID), b"1", qos=2, retain=True)

        self.mqtt.message_callback_add(TOPIC_LAMP_CHANGE_NOTIFICATION,   self.receive_new_lamp_state)
        self.mqtt.message_callback_add(broker_bridge_connection_topic(), self.receive_bridge_connection_status)
        self.mqtt.message_callback_add(TOPIC_LAMP_ASSOCIATED,            self.receive_associated)

        self.mqtt.subscribe(broker_bridge_connection_topic(), qos=1)
        self.mqtt.subscribe(TOPIC_LAMP_CHANGE_NOTIFICATION, qos=1)
        self.mqtt.subscribe(TOPIC_LAMP_ASSOCIATED, qos=2)

    def _poll_associated(self, dt):
        # this polling loop allows us to synchronize changes from the
        #  MQTT callbacks (which happen in a different thread) to the
        #  Kivy UI
        print("lampi_sphinx_app _poll_associated")
        self.device_associated = self._associated

    def receive_associated(self, client, userdata, message):
        print("lampi_sphinx_app receive_assocaited")
        # this is called in MQTT event loop thread
        new_associated = json.loads(message.payload.decode('utf-8'))
        if self._associated != new_associated['associated']:
            if not new_associated['associated']:
                self.association_code = new_associated['code']
            else:
                self.association_code = None
            self._associated = new_associated['associated']

    def on_device_associated(self, instance, value):
        if value:
            self.associated_status_popup.dismiss()
        else:
            self.associated_status_popup.open()

    def update_popup_associated(self, instance):
        code = self.association_code[0:6]
        instance.content.text = ("Please use the\n"
                                 "following code\n"
                                 "to associate\n"
                                 "your device\n"
                                 "on the Web\n{}".format(code)
                                 )

    def receive_bridge_connection_status(self, client, userdata, message):
        print("lampi_sphinx_app receive_bridge_connection_status", userdata, message)
        # monitor if the MQTT bridge to our cloud broker is up
        if message.payload == b"1":
            self.mqtt_broker_bridged = True
        else:
            self.mqtt_broker_bridged = False

    def update_new_config(self, config):
        msg = {'color': {'h': self.hue, 's': self.saturation},
               'brightness': self.brightness,
               'on': self.lamp_is_on,
               'client': MQTT_CLIENT_ID}

        print("DEBUG update_new_config", config)
        print("current config:", msg)
        for piece in config:
            if type(piece) == type({}):
                print("piece", piece)
                for key in piece.keys():
                    if 'h' == key:
                        print("Setting hue to:", piece[key])
                        self.hue = piece[key]
                    if 's' == key:
                        print("Setting sat to:", piece[key])
                        self.saturation = piece[key]
                    if 'b' == key:
                        print("Setting brightness to:", piece[key])
                        self.brightness = piece[key]
            elif type(piece) == type(""):
                if piece.find("LAMPI SET POWER") != -1:
                    if piece.find("0") != -1:
                        self.lamp_is_on = False
                    elif piece.find("1") != -1:
                        self.lamp_is_on = True
                    else: print("Can't detect piece1!", piece)
                elif piece.find("TOGGLE") != -1:
                    self.lamp_is_on = not self.lamp_is_on
            else: print("Can't detect piece2!", piece)

        msg = {'color': {'h': self.hue, 's': self.saturation},
               'brightness': self.brightness,
               'on': self.lamp_is_on,
               'client': MQTT_CLIENT_ID}

        self._update_leds()
        print("config now:", msg)
        #embed()
        #    if 'color' in new_state:
        #        self.hue = new_state['color']['h']
        #        self.saturation = new_state['color']['s']
        #    if 'brightness' in new_state:
        #        self.brightness = new_state['brightness']
        #    if 'on' in new_state:
        #        self.lamp_is_on = new_state['on']


    def receive_new_lamp_state(self, client, userdata, message):
        print("lampi_sphinx_app receive_new_lamp_state", userdata, message)
        #embed()
        new_state = json.loads(message.payload.decode('utf-8'))
        self._update_ui(new_state)
        #Clock.schedule_once(lambda dt: self._update_ui(new_state), 0.01)
        print("updateUI Scheduled!")

    def _update_ui(self, new_state):
        print("lamp_sphinx_app _update_ui", new_state)
        if self._updated and new_state['client'] == MQTT_CLIENT_ID:
            # ignore updates generated by this client, except the first to
            #   make sure the UI is syncrhonized with the lamp_service
            return
        try:
            if 'color' in new_state:
                self.hue = new_state['color']['h']
                self.saturation = new_state['color']['s']
            if 'brightness' in new_state:
                self.brightness = new_state['brightness']
            if 'on' in new_state:
                self.lamp_is_on = new_state['on']
        finally:
            pass

        self._updated = True

    def _update_leds(self):
        msg = {'color': {'h': self.hue, 's': self.saturation},
               'brightness': self.brightness,
               'on': self.lamp_is_on,
               'client': MQTT_CLIENT_ID}
        self.mqtt.publish(TOPIC_SET_LAMP_CONFIG,
                          json.dumps(msg).encode('utf-8'),
                          qos=1)
        self._publish_clock = None

print("lampi_sphinx_app included")
