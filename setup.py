#!/usr/bin/env python

################################################################################
#
# Copyright (c) 2010 Randy Secrist
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License. 
#
################################################################################



from distutils.core import setup, Command, Extension
import mdns

# Grab the description from the package's doc string
desc = mdns.__doc__.strip().split('\n\n')

setup(
    name = 'mdns',
    version = mdns.__version__,
    author = 'Randy Secrist',
    author_email = 'randy.secrist@gmail.com',
    url = 'http://github.com/randysecrist/py-mdns',
    description = desc[0].strip(),
    long_description = mdns.__doc__.strip(),
    download_url = 'http://github.com/randysecrist/py-mdns/downloads',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Networking',
    ],
    packages = ['mdns','mdns.avahi','mdns.bonjour'],
)
