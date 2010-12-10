# module dependencies
import libxml2
import os
import StringIO
from string import Template

# publisher dependencies
from avahi.ServiceTypeDatabase import ServiceTypeDatabase
from mdns.service import servicegroup, service

# resolver dependencies
import dbus, gobject, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop

class Backend:
    __file_location = '/etc/avahi/services/mdns.service'
    
    # the thread which does resolution
    __thread = None
    
    # resolution results
    __results = []
    
    # server callback
    __server_callback = None
    
    def types(self):
        db = ServiceTypeDatabase()
        return db.items()

    def load_group(self, alternate_location=None):
        if alternate_location != None:
            self.__file_location = alternate_location
        doc = libxml2.parseFile(self.__file_location)
        ctx = doc.xpathNewContext()

        sg = servicegroup()

        name_node = ctx.xpathEval('//service-group/name')[0]
        sg.name = name_node.content
        sg.replace = name_node.hasProp('replace-wildcards').content

        service_nodes = ctx.xpathEval('//service-group/service')
        for node in service_nodes:
            ctx.setContextNode(node)
            s = service()
            sg.services.append(s)
            s.type = ctx.xpathEval('type')[0].content
            s.port = int(ctx.xpathEval('port')[0].content)
            record_nodes = ctx.xpathEval('txt-record')
            
            #print type + "::" +  port + "::" + str(len(record_nodes))
            for r_node in record_nodes:
                node_str = r_node.content
                key = node_str[0:node_str.find('=')]
                value = node_str[node_str.find('=') + 1:len(node_str)]
                if key == 'sysname':
                    s.sysname = value
                elif key == 'state':
                    s.state = value
                else:
                    s.txt[key] = value
       
        doc.freeDoc()
        ctx.xpathFreeContext()
        return sg
    
    def save_group(self, servicegroup, alternate_location=None):
        #libxml2.debugMemory(1)
        
        if alternate_location != None:
            self.__file_location = alternate_location
        
        input = '<!DOCTYPE service-group SYSTEM "avahi-service.dtd"><!-- See avahi.service(5) for more information about this configuration file --><service-group></service-group>'
        
        doc = libxml2.parseDoc(input)
        ctx = doc.xpathNewContext()
        root = ctx.xpathEval("/service-group")[0]
        
        name_node = libxml2.newNode('name')
        if servicegroup.replace:
            name_node.setProp('replace-wildcards','yes')
        else:
            name_node.setProp('replace-wildcards', 'no')
        name_node.setContent(servicegroup.name)
        root.addChild(name_node)
        for service in servicegroup.services:
            s_node = libxml2.newNode('service')
            s_node.setProp('protocol', service.protocol)
            ''' state, sysname, localized_name '''

            # type
            type_node = libxml2.newNode('type')
            type_node.setContent(service.type)
            
            #port
            port_node = libxml2.newNode('port')
            port_node.setContent(str(service.port))
            
            s_node.addChild(type_node)
            s_node.addChild(port_node)

            # text records
            for txt in service.txt:
                node = libxml2.newNode('txt-record')
                node.setContent(txt + '=' + service.txt[txt])
                s_node.addChild(node)

            if service.sysname != None:
                node = libxml2.newNode('txt-record')
                node.setContent('sysname' + '=' + service.sysname)
                s_node.addChild(node)
            
            if service.state != None:
                node = libxml2.newNode('txt-record')
                node.setContent('state' + '=' + service.state)
                s_node.addChild(node)
            
            root.addChild(s_node)

        rtnval = -1
        try:
            outfile = open(self.__file_location, 'w')
            rtnval = doc.saveFormatFile(self.__file_location, format=libxml2.XML_SAVE_FORMAT)
            #f = StringIO.StringIO()
            #buf = libxml2.createOutputBuffer(f, 'UTF-8')
            #doc.saveFormatFileTo(buf, 'UTF-8', 1)
            #print repr(f.getvalue())
        finally:
            doc.freeDoc()
            ctx.xpathFreeContext()
        '''
        libxml2.cleanupParser()
        if libxml2.debugMemory(1) == 0:
            print "OK"
        else:
            print "Memory leak %d bytes" % (libxml2.debugMemory(1))
            libxml2.dumpMemory()
        '''
        return rtnval

    def remove_group(self, alternate_location=None):
        if alternate_location != None:
            self.__file_location = alternate_location
        os.remove(self.__file_location)
        return os.path.exists(self.__file_location)
        
    def query(self, type=None):
        # clear any prior state
        self.__results = []
        self.__thread = None
        self.__server_callback = None
        
        # establish dbus context
        # no need to cache (yet), object should be short term lifecycle
        self.__thread = gobject.MainLoop()
        bus = dbus.SystemBus(mainloop=DBusGMainLoop())
        
        # lookup server instance
        # if = org.freedesktop.Avahi.Server
        self.__server_callback = dbus.Interface(
            bus.get_object(avahi.DBUS_NAME, '/'),
            avahi.DBUS_INTERFACE_SERVER
        )
        
        # determine the network interface to do this on
        nic = self.__server_callback.ServiceBrowserNew(
            avahi.IF_UNSPEC,
            avahi.PROTO_UNSPEC,
            type,
            'local',
            dbus.UInt32(0)
        )
        
        # lookup service browser
        # if = org.freedesktop.Avahi.ServiceBrowser
        sbrowser = dbus.Interface(
            bus.get_object(avahi.DBUS_NAME, nic),
            avahi.DBUS_INTERFACE_SERVICE_BROWSER
        )
        
        # setup signal handlers
        sbrowser.connect_to_signal("ItemNew", self.__handle_service_new)
        sbrowser.connect_to_signal("ItemRemove", self.__handle_service_remove)
        sbrowser.connect_to_signal("AllForNow", self.__handle_all_for_now)
        
        # asynch collect results
        self.__thread.run()
        
        # filter results by query type
        # (results will be populated by now)
        # pair down by text record or however you want it done
        # (build this into a function call to keep this method from turning into a monster)
        
        return self.__results
        
    def __handle_all_for_now(self):
        self.__thread.quit()
    
    def __handle_service_new(self, interface, protocol, name, stype, domain, flags):
        #print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)
        
        # local service, skip
        if flags & avahi.LOOKUP_RESULT_LOCAL:
            pass
        
        # construct service record
        self.__server_callback.ResolveService(interface, protocol, name, stype, 
                              domain, avahi.PROTO_UNSPEC, dbus.UInt32(0), 
                              reply_handler=self.__service_resolved,
                              error_handler=self.__print_error)
    
    '''
    Asynchronous Event Handlers for DBUS
    '''
    def __handle_service_remove(self, interface, protocol, name, stype, domain, flags):
        #print "Remove service '%s' type '%s' domain '%s' " % (name, stype, domain)
        pass
        
    def __service_resolved(self, *args):
        '''
        print 'service resolved'
        print 'name:', args[2]
        print 'type:', args[3]
        print 'domain:', args[4]
        print 'full_domain:', args[5]
        print 'address:', args[7]
        print 'port:', args[8]
        print avahi.txt_array_to_string_array(args[9])
        '''
        
        # construct service
        s = service()
        s.type = args[3]
        s.port = int(args[8])
        
        txt_records = avahi.txt_array_to_string_array(args[9])
        for record in txt_records:
            key = record[0:record.find('=')]
            value = record[record.find('=') + 1:len(record)]
            if key == 'sysname':
                s.sysname = value
            elif key == 'state':
                s.state = value
            else:
                s.txt[key] = value
        
        # add service to results
        self.__results.append(s)

    def __print_error(self, *args):
        print 'error_handler'
        print args[0]
