import gi
from gi.repository import Gtk
gi.require_version('WebKit', '3.0')
from gi.repository import WebKit


class BrowserView(object):
    def __init__(self):
        window = Gtk.Window()
        window.connect('delete-event', Gtk.main_quit)

        browser = WebKit.WebView()
        browser.load_uri('http://127.0.0.1:5000/report/2014/01')

        scroller = Gtk.ScrolledWindow()
        vbox = Gtk.VBox(False)
        window.add(vbox)
        vbox.pack_start(scroller, True, True, 0)
        scroller.add(browser)

        window.show_all()
        window.resize(800, 800)


if __name__ == "__main__":
    BrowserView()
    Gtk.main()
