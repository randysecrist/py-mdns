import libxml2
import os
import StringIO
from string import Template
from avahi.ServiceTypeDatabase import ServiceTypeDatabase

class Backend():
    def types(self):
        db = ServiceTypeDatabase()
        return db.items()
    
    def publish_group(self, servicegroup):
        libxml2.debugMemory(1)
        
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
            
            root.addChild(s_node)

        rtnval = -1
        try:
            #file_loc = '/home/de041669/test.xml'
            file_loc = '/etc/avahi/services/cks.service'
            outfile = open(file_loc, 'w')
            rtnval = doc.saveFormatFile(file_loc, format=libxml2.XML_SAVE_FORMAT)
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

    def publish(self, service):
        DOC="""<?xml version="1.0" standalone='no'?><!--*-nxml-*-->
        <!DOCTYPE service-group SYSTEM "avahi-service.dtd">
        
        <!-- $Id$ -->
        
        <!-- See avahi.service(5) for more information about this configuration file -->
        
        <service-group>
        
          <name replace-wildcards="yes">$localized_name - %h</name>
        
          <service protocol="$protocol">
            <type>$type</type>
            <port>$port</port>
            <!--
            <subtype>_anon._sub._ftp._tcp</subtype>
            <host-name>%h</host-name>
            <domain-name>.local</domain-name>
            -->
            <txt-record>state=$state</txt-record>
            <txt-record>sysname=$sysname</txt-record>
          </service>
        
        </service-group>
        """

        d = dict(sysname=service.sysname,
                 localized_name=service.localized_name,
                 protocol=service.protocol,
                 type=service.type,
                 port=service.port,
                 state=service.state)
        template = Template(DOC)
        DOC = template.safe_substitute(d)
        
        doc = libxml2.parseDoc(DOC)
        ctx = doc.xpathNewContext()
        root = ctx.xpathEval("//service-group/service")[0]
        
        #add text records if any exist
        child = root.children
        for txt in service.txt:
            node = libxml2.newNode('txt-record')
            node.setContent(txt + '=' + service.txt[txt])
            child.addSibling(node)

        # write the file
        rtnval = -1
        try:
            f_name = str(hash(service))
            outfile = open('/etc/avahi/services/' + f_name + '.service', 'w')
            rtnval = doc.saveTo(outfile)
            outfile.close()
        finally:
            doc.freeDoc()

        return rtnval
    
    def remove(self, service):
        f_name = str(hash(service))
        os.remove('/etc/avahi/services/' + f_name + '.service')
        if os.path.exists('/etc/avahi/services/' + f_name + '.service'):
            return 1
        else:
            return 0
