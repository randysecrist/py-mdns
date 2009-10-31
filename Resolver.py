import dbus, gobject, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop

# Looks for iTunes shares
#TYPE = '_daap._tcp'

# Looks for HTTP
TYPE = '_http._tcp'

# Looks for HTTPS
#TYPE = '_https._tcp'

def service_resolved(*args):
    print 'service resolved'
    print 'name:', args[2]
    print 'address:', args[7]
    print 'port:', args[8]
    print avahi.txt_array_to_string_array(args[9])

def print_error(*args):
    print 'error_handler'
    print args[0]
    
def handle_service_new(interface, protocol, name, stype, domain, flags):
    print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)

    if flags & avahi.LOOKUP_RESULT_LOCAL:
            # local service, skip
            pass

    server.ResolveService(interface, protocol, name, stype, 
        domain, avahi.PROTO_UNSPEC, dbus.UInt32(0), 
        reply_handler=service_resolved, error_handler=print_error)

def handle_service_remove(interface, protocol, name, stype, domain, flags):
    print "Remove service '%s' type '%s' domain '%s' " % (name, stype, domain)

loop = DBusGMainLoop()

bus = dbus.SystemBus(mainloop=loop)

server = dbus.Interface( bus.get_object(avahi.DBUS_NAME, '/'),
        'org.freedesktop.Avahi.Server')

sbrowser = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
        server.ServiceBrowserNew(avahi.IF_UNSPEC,
            avahi.PROTO_UNSPEC, TYPE, 'local', dbus.UInt32(0))),
        avahi.DBUS_INTERFACE_SERVICE_BROWSER)

sbrowser.connect_to_signal("ItemNew", handle_service_new)
sbrowser.connect_to_signal("ItemRemove", handle_service_remove)

gobject.MainLoop().run()
