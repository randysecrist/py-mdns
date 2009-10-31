#!/usr/bin/python

import os, sys

try:
    import avahi, dbus, avahi.ServiceTypeDatabase
except ImportError, e:
    print "Sorry, to use this tool you need to have Avahi and python-dbus.\n Error: %s" % e
    sys.exit(1)
    
try:
    from dbus import DBusException
    import dbus.glib
except ImportError, e:
    pass

service_type_browsers = {}
service_browsers = {}
service_type_db = avahi.ServiceTypeDatabase.ServiceTypeDatabase()

def error_msg(msg):
    print msg
    
class EventHandlers():
    def new_service_type(self, interface, protocol, stype, domain, flags):
        print "--- New Service Type Called! ---"
        
        
def main():
    handlers = EventHandlers()
    # line 234, 235 of avahi-discover
    # setup dbus
    bus = dbus.SystemBus()
    server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), avahi.DBUS_INTERFACE_SERVER)
    try:
        # how do we know to limit this range?
        # which NIC do we listen on?
        # do we even need to do this?
        for i in range(1, 8):
            x = server.GetNetworkInterfaceNameByIndex(i)
            print x
    except DBusException, e:
        print "Intentional Error: \"%s\"" % e

    domain = "local"
    try:
        # browse for services
        interface = avahi.IF_UNSPEC
        protocol = avahi.PROTO_UNSPEC
        b = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.ServiceTypeBrowserNew(interface, protocol, domain, dbus.UInt32(0))), avahi.DBUS_INTERFACE_SERVICE_TYPE_BROWSER)

        # register for dbus events
        #b.connect_to_signal('ItemNew', self.new_service_type)
        # line 168 of avahi-discover
        # basically - sets up a function pointer to ItemNew signal
        b.connect_to_signal('ItemNew', handlers.new_service_type)
        
        service_type_browsers[(interface, protocol, domain)] = b
        # do we have to do anything else to start up the listener?
        print service_type_browsers

    except DBusException, e:
        print "DBusException - %s" % e
        sys.exit(0)

if __name__ == "__main__":
    main()
    import time
    time.sleep(15)
    print "All Done!"
