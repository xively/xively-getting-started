# Copyright (c) 2003-2015, Xively. All rights reserved.
# This is part of Xively Python library.

class XivelyConnectionParameters:

    """XivelyClient Connection parameters"""

    def __init__(self):

        self.username = None
        self.password = None

        self.client_id = None
        self.keep_alive = 60
        self.clean_session = False
        self.connection_timeout = 10

        self.will_qos = 0
        self.will_topic = None
        self.will_retain = False
        self.will_message = None

        self.use_websocket = False

        self.publish_count_send_time_period = 0

