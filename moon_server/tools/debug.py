# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

def logger(func):
    def inner(*args, **kwargs):
        print("\033[35m{}\033[m( {}, {} )".format(func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return inner


def print_args(*args, **kwargs):
    for arg in args:
        print("{}={}".format(eval("'arg'"), arg))
    for arg in kwargs.keys():
        print("{}={}".format(arg, kwargs[args]))