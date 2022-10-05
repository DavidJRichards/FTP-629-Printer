from escpos import *
from textwrap import *
import configparser

import gi
from gi.repository import GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import datetime
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import json

wrapper = TextWrapper(width=32,break_long_words=False,replace_whitespace=False)
config = configparser.ConfigParser()
config.read('mqtt-print.ini')

mqtt_server = config['MQTT'].get('Server')
mqtt_port = config['MQTT'].getint('Port')
mqtt_topic = config['MQTT'].get('Topic')
mqtt_use_auth = config['MQTT'].getboolean('Auth')
mqtt_use_tls = config['MQTT'].getboolean('TLS')

printer_file = config['Printer'].get('PrinterFile')

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


def print_notification(bus, message):
  client1= paho.Client("control1")                           #create client object
#  client1.on_publish = on_publish                          #assign function to callback
  client1.connect(mqtt_server,mqtt_port)                                 #establish connection

  keys = ["app_name", "replaces_id", "app_icon", "summary",
          "body", "actions", "hints", "expire_timeout"]
  args = message.get_args_list()

  if len(args) == 8:
    now = datetime.datetime.now()
#    print (now.strftime("%Y-%m-%d %H:%M:%S"), " ", end='')  
    notification = dict([(keys[i], args[i]) for i in range(8)])

    ret= client1.publish(mqtt_topic + "/date",now.strftime("%Y-%m-%d %H:%M:%S"))      #publish
    ret= client1.publish(mqtt_topic + "/summary", notification["summary"])                   #publish
    ret= client1.publish(mqtt_topic + "/body",notification["body"])                   #publish

    my_json_string = json.dumps({'date': now.strftime("%Y-%m-%d %H:%M:%S"), 'summary': notification["summary"], 'body': notification["body"]})
    ret= client1.publish(mqtt_topic, my_json_string)      #publish

    summary_string = now.strftime("%Y-%m-%d %H:%M:%S") + " " + notification["summary"]
    print(summary_string)
    if len(summary_string) > 150:
        summary_string = summary_string[:150]        
    summary_string = wrapper.fill(summary_string)

    body_string = notification["body"]
    print(body_string)
    if len(body_string) > 400:
        body_string = body_string[:400]        
    body_string = wrapper.fill(body_string)

    prt = printer.File(printer_file)        # comment to disable ticket printing
    prt.hw("init")
    prt.text('{0}'.format(summary_string))   
    prt.text('\n--------------------------------\n')
    prt.text('{0}'.format(body_string))   
    prt.cut(mode='PART')
    prt = None

loop = DBusGMainLoop(set_as_default=True)
session_bus = dbus.SessionBus()
session_bus.add_match_string("type='method_call',interface='org.freedesktop.Notifications',member='Notify',eavesdrop=true")
session_bus.add_message_filter(print_notification)

GLib.MainLoop().run()
