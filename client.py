#!/usr/bin/python
# Copyright (c) 2003-2015, LogMeIn, Inc. All rights reserved.
# This is part of Xively Python library.
import sys
import os
import codecs

sys.path.append( os.getcwd() )
from xi_client.xively_client import XivelyClient
from xi_client.xively_connection_parameters import XivelyConnectionParameters
from xi_client.xively_error_codes import XivelyErrorCodes as xec

credentialsfilepath = os.path.expanduser('~/Desktop/MQTTCredentials.txt')
topicfilepath       = os.path.expanduser('~/Desktop/MQTTTopic.txt')

retrys_number = 3
username = None
password = None
test_topic = None

def retry_number_gen():
    try_number = 0

    while try_number < retrys_number:
        try_number += 1
        yield try_number

get_connect_try_number = retry_number_gen()

def on_connect_finished(client,result):
    print("on_connect_finished",str(result))

    if result == xec.XI_STATE_OK :
        print( "connected, subscribing to topic" )
        client.subscribe(( test_topic , 0 ))

    else :
        try:
            connect_try_number = next(get_connect_try_number)
        except StopIteration:
            print("Couldnt connect to the endpoint in %d tries, shutting down." % retrys_number)
            sys.exit( -1 )
        print("Connection try %d/%d"  % (connect_try_number, retrys_number))
        print("Connection error :" , result)
        print("Reconnecting to the broker ... ")
        client.connect(params)

def on_disconnect_finished(client,result):
    print("on_disconnect_finished",result)


def on_publish_finished(client,message):
    print("on_publish_finished")


def on_subscribe_finished(client,mid,granted_qos):
    global test_topic

    print("on_subscribe_finished " )
    print( "publishing to topic" )
    client.publish( test_topic, "Hello through xively!!!", 0 , False )


def on_unsubscribe_finished(client,mid):
    print("on_unsubscribe_finished")
    print( "disconnecting" )
    client.disconnect()


def on_message_received(client,message):
    global test_topic

    print("on_message_received",str(message))
    print( "unsubscribing from topic" )
    client.unsubscribe( test_topic )

def u2a( data ):
    return str( codecs.decode( codecs.encode( data, 'ascii', 'ignore' ), 'ascii', 'ignore' ) )

if __name__ == '__main__':
    doExit = False
    client = XivelyClient()
    client.on_connect_finished = on_connect_finished
    client.on_disconnect_finished = on_disconnect_finished
    client.on_publish_finished = on_publish_finished
    client.on_subscribe_finished = on_subscribe_finished
    client.on_unsubscribe_finished = on_unsubscribe_finished
    client.on_message_received = on_message_received

    params = XivelyConnectionParameters()
    params.use_websocket = False
    params.publish_count_send_time_period = 5

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
