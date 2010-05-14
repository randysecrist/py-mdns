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
        svc = service('_http._tcp', 80, 'Web Site', 'training', 'INITIAL')
        search_pattern = svc.type_full
        i = types.index(search_pattern)
        
        # assert match
        self.assertEquals(types[i], svc.type_full)
        
    def test_service_unique(self):
        a = service('_jdbc._tcp', 1521, 'Oracle JDBC', 'training', 'INITIAL')
        b = service('_jdbc._tcp', 1521, 'Oracle JDBC', 'training', 'INITIAL')
        c = service('_jdbc._tcp', 1522, 'Oracle JDBC', 'training', 'INITIAL')
        self.assertEquals(a,b)
        self.assertNotEquals(b,c)
        self.assertEquals(hash(a),hash(b))
        self.assertNotEquals(hash(a),hash(c))
            
    def test_publisher(self):
        # create the services
        svc_a = service('_jdbc._tcp', 1521, 'Oracle JDBC', 'training', 'SCHEMA-READY')
        svc_a.txt = { 'foo':'smoke', 'bar':'monster' }
        
        p = publisher()
        
        # publish it
        p_rtn = p.publish(svc_a)
        
        # remove it
        r_rtn = p.remove(svc_a)

        # assert success
        self.assertTrue(p_rtn >= 0)
        self.assertTrue(r_rtn >= 0)

    def test_resolver(self):
        r = resolver()
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BackendTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
