import libxml2
import os
from avahi.ServiceTypeDatabase import ServiceTypeDatabase

class Backend():
    def types(self):
        db = ServiceTypeDatabase()
        return db.items()
    
    def publish(self, service):
        DOC = """<?xml version="1.0" standalone='no'?><!--*-nxml-*-->
        <!DOCTYPE service-group SYSTEM "avahi-service.dtd">
        
        <!-- $Id$ -->
        
        <!-- See avahi.service(5) for more information about this configuration file -->
        
        <service-group>
        
          <name replace-wildcards="yes">%(sysname)s - %(localized_name)s</name>
        
          <service protocol="%(protocol)s">
            <type>%(type)s</type>
            <port>%(port)s</port>
            <!--
            <subtype>_anon._sub._ftp._tcp</subtype>
            <host-name></host-name>
            <domain-name>.local</domain-name>
            -->
          </service>
        
        </service-group>
        """%{'sysname':service.sysname,
             'localized_name':service.localized_name,
             'protocol':service.protocol,
             'type':service.type,
             'port':service.port}
        
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