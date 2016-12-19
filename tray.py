from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from requests.auth import HTTPBasicAuth
import signal, os, json, requests, sys

APPINDICATOR_ID = 'myappindicator'

def main():
    if(len(sys.argv) < 2):
        print "Room id not set"
        sys.exit()
    room_id = sys.argv[1]
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, 'no icon', appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(gtk.Menu())
#    indicator.set_icon(os.path.abspath('circle_red.png'))
#    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_YES, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
#    gtk.main()
    url = "https://hackathon-heroku-app.herokuapp.com/occupied"
#    response = urllib.urlopen(url)
    response = requests.get(url, auth=HTTPBasicAuth('1', '123456'))
#    data = json.loads(response)
#    print data
    json_arr = response.json()
    occupied = None
    for room in json_arr:
#        print room
        if(room['id'] == int(room_id)):
            print room
            occupied = room['occupied']
    print occupied
    img_path = ""
    if(occupied):
        print "inside occupied"
        img_path = os.path.abspath('circle_red.png')
    elif(occupied == False):
        print "inside not occupied"
        img_path = os.path.abspath('circle_green.png')
    else:
        print "inside unknown"
        img_path = os.path.abspath('unknown.png')
    print img_path
    indicator.set_icon(img_path)
    gtk.main()

if __name__ == "__main__":
    main()
