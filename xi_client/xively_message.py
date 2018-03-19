# Copyright (c) 2003-2015, Xively. All rights reserved.
# This is part of Xively Python library.

class XivelyMessage:

    """XivelyMessage class is for encapsulating message parameters"""

    def __init__(self):

        """
        qos -- The QoS level of the QoS message, based on the MQTT specification.
        topic -- A string that represents the subscribed topic that was used to deliver the message to the
        Xively Client.
        payload -- A bytearray containing the payload of the incoming message.
        request_id -- The identifier of the publish request."""

        self.qos = 0
        self.topic = ""
        self.payload = None
        self.request_id = 0

    def __str__(self):

        return "topic: " + str( self.topic) + " payload: " + str( self.payload ) + " qos: " + str( self.qos ) + " request_id: " + str( self.request_id )
