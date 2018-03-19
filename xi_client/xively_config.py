# Copyright (c) 2003-2015, Xively. All rights reserved.
# This is part of Xively Python library.

from .control_pb2 import Message

class XivelyConfig:

    XI_MQTT_CERTS = [ "GlobalSign Root CA.pem" , "GeoTrust Primary Certification Authority - G3.pem" , "thawte Primary Root CA - G3.pem" , "VeriSign Class 3 Public Primary Certification Authority - G5.pem" , "xi_RootCA_list.pem" ]
    XI_MQTT_HOSTS = [ ("broker.xively.com", 8883, True) ]
    XI_MQTT_WEBSOCKET_PORT = 443

    def on_connect_finished(self,result):

        pass


    def on_disconnect_finished(self,result):

        pass


    def on_message_received(self,message):

        mymessage = Message()
        mymessage.ParseFromString(message.payload)

