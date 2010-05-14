import avahi
import dbus

__all__ = ["Publisher"]

class Publisher:
    """
    A simple class to publish a network service with zeroconf using avahi.

    """

    def __init__(self, name, port, stype="",
                 domain="", host="", text=""):
        self.name = name
        self.stype = stype
        self.domain = domain
        self.host = host
        self.port = port
        self.text = text
    
    def publish(self):
        bus = dbus.SystemBus()
        server = dbus.Interface(
                         bus.get_object(
                                avahi.DBUS_NAME,
                                avahi.DBUS_PATH_SERVER),
                                avahi.DBUS_INTERFACE_SERVER)

        g = dbus.Interface(
                    bus.get_object(avahi.DBUS_NAME,
                           server.EntryGroupNew()),
                           avahi.DBUS_INTERFACE_ENTRY_GROUP)

        g.AddService(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC,dbus.UInt32(0),
                     self.name, self.stype, self.domain, self.host,
                     dbus.UInt16(self.port), self.text)

        g.Commit()
        self.group = g
    
    def unpublish(self):
        self.group.Reset()


def test():
    text = ['FOO=A', 'BAR=B']
    service = Publisher(name="TestService", port=3000, stype="_http._tcp", text=text)
    service.publish()
    input = raw_input("Press any key to unpublish the service --> ")
    print 'Input: %s detected - exiting ...' % input
    service.unpublish()


if __name__ == "__main__":
    test()
