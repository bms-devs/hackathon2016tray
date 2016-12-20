import os
import requests
import signal
import sys
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib as glib
from gi.repository import Gtk as gtk
from requests.auth import HTTPBasicAuth

APPINDICATOR_ID = 'myappindicator'


def update(room_id, indicator):
    url = "https://hackathon-heroku-app.herokuapp.com/occupied"
    response = requests.get(url, auth=HTTPBasicAuth('1', '123456'))
    json_arr = response.json()
    occupied = None
    for room in json_arr:
        if room['id'] == int(room_id):
            print room
            occupied = room['occupied']
    if occupied:
        img_path = os.path.abspath('circle_red.png')
    elif not occupied:
        img_path = os.path.abspath('circle_green.png')
    else:
        img_path = os.path.abspath('unknown.png')
    indicator.set_icon(img_path)
    return True


def main():
    if(len(sys.argv) < 2):
        print "Room id not set. Pass room id as the first argument of the script, e.g. 'python tray.py 1'"
        sys.exit()
    room_id = sys.argv[1]
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('unknown.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(gtk.Menu())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    update(room_id, indicator)
    glib.timeout_add_seconds(5, update, room_id, indicator)
    gtk.main()

if __name__ == "__main__":
    main()
