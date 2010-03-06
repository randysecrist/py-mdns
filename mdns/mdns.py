################################################################################
#
# Copyright (c) 2010 Randy Secrist
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################


"""

Pure-Python interface to Apple Bonjour and compatible DNS-SD libraries

mdns provides a pure-Python interface to DNS-SD libraries such as
Apple Bonjour and Avahi.  It allows consuming Python programs to
take advantage of compliant Zero Configuration Networking (Zeroconf)
to register, discover, and resolve service on both local and wide-area
networks.

In the sprit of zero configuration, this Python mdns module is relies
on the underlying operating system to provide natural support for
DNS-SD operations.  For example; when using this module on a machine
which runs Linux, the Avahi backend will be used.  When using this
module on a machine using Mac OS X, the Apple Bonjour backend will
be used via Christopher Stawarz's pybonjour python module.

This design decision was born from the idea of providing a quick and
easy mechanism which can be hooked to operating system services (such
as those found in Linux under /etc/init.d).  These services once active
would optionally export DNS-SD information to the local vlan.

Additionally providing a neutral DNS abstraction in front of Avahi and
Bonjour serves to protect downstream applications and scripts from
changing specifications as DNS-SD becomes more mainstream and makes its
way through the IETF.

For more information on the Internet Standards draft please visit:
  http://files.multicastdns.org/draft-cheshire-dnsext-multicastdns.txt

"""

# public symbols
__all__ = [ "mdns" ]

__author__   = 'Randy Secrist <randy.secrist@gmail.com>'
__version__  = '1.0.0'
__revision__ = int('$Revision: 1 $'.split()[1])

# Public API
# TODO:
#    Fix module import semantics.
#      add unit tests
#    Load backend.
#    Plug it in.
#    Return
#    Test Cases
#    Documentation & Examples

mdns = None

import imputil
import os
import sys

def publish():
    print "Publish Info"

def resolve():
    print "Resolve Info"
	
def __determine_backend():
    platform = sys.platform
    backend = None
    if platform == 'darwin':
        backend = 'bonjour'
    elif platform.startswith('linux'):
        backend = 'avahi'
    else:
        raise NotImplementedError, "py-mdns is only supported on OS X and Linux."

    assert (backend != None)
    return backend

def __load_backend(backend_name):
    if os.access(backend_name, os.R_OK):
        path = backend_name
        
    # append the location of the library to the python path so we can import
    sys.path.insert(0, path)
    
    b_interface_name = 'interface'
    
    # find the module
    try:
        exists = imputil.imp.find_module(b_interface_name)
    except:
        print "module import of %s failed: %s" % (b_interface_name, sys.exc_type)
    
    # load the module
    retval = None
    try:
        loaded = imputil.imp.load_module(b_interface_name, exists[0], exists[1], exists[2])
        retval = loaded
    except:
        print "module load of %s failed: %s" % (b_interface_name, sys.exc_type)
        
    return retval
        
if __name__ == "__main__":
    backend_name = __determine_backend()
    print backend_name
    backend = __load_backend(backend_name)
