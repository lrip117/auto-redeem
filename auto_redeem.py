import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction
from time import sleep


# --------------------------------------

PLACE_FURNI = 1258
REDEEM = 3115
SPEECH_OUT = 1314
SPEECH_IN = 1797

# --------------------------------------


extension_info = {
    "title": "Auto Redeem",
    "description": "!ar",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()


on = False


def speech(msg):
    global on
    (text, color, index) = msg.packet.read('sii')
    if text == '!ar':
        msg.is_blocked = True
        message(' Use `!ar on` or `!ar off` ')
    if text == '!ar on':
        msg.is_blocked = True
        on = True
        message(' Auto Redeem On ')
    if text == '!ar off':
        msg.is_blocked = True
        on = False
        message(' Auto Redeem Off ')


def furni(msg):
    if on:
        s = msg.packet.read_string()
        s = s.split(" ", 1)[0]
        sleep(1)
        ext.send_to_server('{l}{h:'+str(REDEEM)+'}{i:'+str(s)+'}')


def message(msg):
    ext.send_to_client('{l}{h:'+str(SPEECH_IN)+'}{i:0}{s:"'+msg+'"}{i:0}{i:1}{i:0}{i:0}')


ext.intercept(Direction.TO_SERVER, speech, SPEECH_OUT)
ext.intercept(Direction.TO_SERVER, furni, PLACE_FURNI, mode='async')
