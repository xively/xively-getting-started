#!/usr/bin/python
# Copyright (c) 2003-2015, LogMeIn, Inc. All rights reserved.
# This is part of Xively Python library.
import sys
import os
import codecs
import time
import random
import math
from datetime import datetime

from xi_client.xively_client import XivelyClient
from xi_client.xively_connection_parameters import XivelyConnectionParameters
from xi_client.xively_error_codes import XivelyErrorCodes as xec

credentialsfilepath = os.path.expanduser('~/Desktop/MQTTCredentials.txt')
topicfilepath       = os.path.expanduser('~/Desktop/MQTTTopic.txt')

retrys_number = 3
username = None
password = None
test_topic = None

def pi_gen():
    iteration = 0
    count_inside = 0

    while True:
        for i in range(0, 100):
            iteration += 1

            d = math.hypot( random.random(), random.random() )

            if d < 1:
                count_inside += 1

        yield iteration, str( 4.0 * count_inside / iteration )

def retry_number_gen():
    try_number = 0

    while try_number < retrys_number:
        try_number += 1
        yield try_number

get_connect_try_number = retry_number_gen()
get_pi_evaluation = pi_gen()

def publish_message(client, topic):
    iterations, value = next(get_pi_evaluation)
    message = "Hello through Xively with pi estimation after iteration: " \
        + str(iterations) + " value: " + value + " and timestamp = " \
        + str(datetime.now()) + "!!!"
    client.publish(topic, message, 0, False)

def on_connect_finished(client,result):
    print("on_connect_finished",str(result))

    if result == xec.XI_STATE_OK :
        print( "connected, starting to publish" )
        publish_message(client, test_topic)

    else :
        try:
            connect_try_number = next(get_connect_try_number)
        except StopIteration:
            print("Couldnt connect to the endpoint in %d tries, shutting down." % retrys_number)
            sys.exit(-1)
        print("Connection try %d/%d"  % (connect_try_number, retrys_number))
        print("Connection error :" , result)
        print("Reconnecting to the broker ... ")
        client.connect(params)

def on_disconnect_finished(client,result):
    print("on_disconnect_finished",result)

def on_publish_finished(client,message):
    print("on_publish_finished")
    time.sleep( 1 )
    publish_message(client, test_topic)

def u2a( data ):
    return str( codecs.decode( codecs.encode( data, 'ascii', 'ignore' ), 'ascii', 'ignore' ) )

if __name__ == '__main__':
    doExit = False
    client = XivelyClient()
    client.on_connect_finished = on_connect_finished
    client.on_disconnect_finished = on_disconnect_finished
    client.on_publish_finished = on_publish_finished

    params = XivelyConnectionParameters()

    try:
        with codecs.open(credentialsfilepath, 'r', encoding='utf8') as credsfile:
            password = u2a(credsfile.readline().rstrip('\n'))
            username = u2a(credsfile.readline().rstrip('\n'))
    except (IOError, OSError) as e:
        print( e )
        sys.exit( 0 )

    print( "Read username and password from the file %s" %(credentialsfilepath))
    print ( "Username = %s" %(username))
    print ( "Password = %s" %(password))

    try:
        with codecs.open(topicfilepath, 'r', encoding='UTF-8') as topicfile:
            test_topic = u2a(topicfile.readline().rstrip('\n'))
    except (IOError, OSError) as e:
        print( e )
        sys.exit( 0 )

    print( "Read topic name from the file %s" %(topicfilepath))
    print ( "Topic = %s" %(test_topic))

    params.client_id = username
    params.username = username
    params.password = password

    print( "Connecting to the correct broker ... ")
    client.connect(params)
