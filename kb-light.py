#!/usr/bin/env python

import dbus
import time
from sys import argv

from gi import require_version
require_version('Notify', '0.7')
from gi.repository import Notify


def kb_light_set(delta):
    bus = dbus.SystemBus()
    kbd_backlight_proxy = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower/KbdBacklight')
    kbd_backlight = dbus.Interface(kbd_backlight_proxy, 'org.freedesktop.UPower.KbdBacklight')

    val = kbd_backlight.GetBrightness()
    kmax = kbd_backlight.GetMaxBrightness()

    new = max(0, val + delta)
    if new >= 0 and new <= kmax:
        val = new
        kbd_backlight.SetBrightness(val)
    return 100 * val / kmax


def kb_light_inc():
    percent = kb_light_set(1)
    display_notification(percent)
    return percent


def kb_light_dec():
    percent = kb_light_set(-1)
    display_notification(percent)
    return percent


def display_notification(percent):
    Notify.init("Keyboard backlight changer")
    kb_light_notify=Notify.Notification.new("Keyboard backlight", "Set to " + str(int(percent)) + "%", "dialog-information")
    kb_light_notify.set_timeout(3)
    kb_light_notify.show()
    Notify.uninit()


if len(argv[1:]) == 1:
    if argv[1] == "--up" or argv[1] == "+":
        kb_light_inc()
    elif argv[1] == "--down" or argv[1] == "-":
        kb_light_dec()
    else:
        print("Unknown argument: " + argv[1])
else:
    print("Script takes exactly one argument." + len(argv[1:]) +  "provided.")

