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
__revision__ = int('$Revision: 6125 $'.split()[1])

# Public API
# TODO:
#    Determine which backend to load.
#      avahi, bonjour
#    Load backend.
#    Plug it in.
#    Return
#    Test Cases
#    Documentation & Examples
def publish():
    print "Publish Info"

def resolve():
    print "Resolve Info"