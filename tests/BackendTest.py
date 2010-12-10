import os
import random
import unittest

from mdns import loader,publisher,resolver
from mdns.service import servicegroup, service

class BackendTest(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_types(self):
        # load db
        backend = loader().get_backend()
        types = backend.types()
        
        # search it
        svc = service(type='_http._tcp', port=80, name='Web Site',
                      sysname='training', state='INITIAL')
        search_pattern = svc.type_full
        i = types.index(search_pattern)
        
        # assert match
        self.assertEquals(types[i], svc.type_full)
        
    def test_service_unique(self):
        a = service(type='_jdbc._tcp', port=1521, name='Oracle JDBC',
                    sysname='training', state='INITIAL')
        b = service(type='_jdbc._tcp', port=1521, name='Oracle JDBC',
                    sysname='training', state='INITIAL')
        c = service(type='_jdbc._tcp', port=1522, name='Oracle JDBC',
                    sysname='training', state='INITIAL')
        self.assertEquals(a,b)
        self.assertNotEquals(b,c)
        self.assertEquals(hash(a),hash(b))
        self.assertNotEquals(hash(a),hash(c))
            
    def test_publisher(self):
        # create the group
        group = servicegroup()
        group.name = 'Test Service Group'

        # create the services
        svc_a = service(type='_jdbc._tcp', port=1521, name='Oracle JDBC',
                        sysname='training', state='SCHEMA-READY')
        svc_a.txt = { 'foo':'smoke', 'bar':'monster' }
        svc_b = service(type='_http._tcp', port=8080, name='Virgo',
                        sysname='training', state='RUNNING')
        group.services = [ svc_a, svc_b ]
        
        p = publisher()
        
        # publish them (seralize)
        if os.geteuid() != 0:
            self.assertRaises(IOError, p.save_group, group)
        else:
            p_rtn = p.save_group(group)
            self.assertTrue(p_rtn >= 0)

            # load service group (deserialize)
            sg = p.load_group()

            self.assertTrue(sg != None)
            self.assertEquals(sg.services[0].protocol, group.services[0].protocol)
            self.assertEquals(sg.services[0].type, group.services[0].type)
            self.assertEquals(sg.services[0].port, group.services[0].port)
            self.assertEquals(sg.services[0].sysname, group.services[0].sysname)
            self.assertEquals(sg.services[0].state, group.services[0].state)
            self.assertEquals(sg.services[0].txt['foo'], group.services[0].txt['foo'])

            # remove it
            r_rtn = p.remove_group()
            self.assertTrue(r_rtn >= 0)

    def test_resolver(self):
        r = resolver()
        #results = r.query('_http._tcp')
        results = r.query('_daap._tcp')
        print len(results)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BackendTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
