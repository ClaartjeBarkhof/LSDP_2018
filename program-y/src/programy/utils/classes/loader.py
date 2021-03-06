"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import importlib

class ClassLoader(object):

    @staticmethod
    def instantiate_class(class_string):
        processor_path = class_string.strip()
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Processor path [%s]", processor_path)

        last_dot = processor_path.rfind(".")
        module_path = processor_path[:last_dot]
        class_name = processor_path[last_dot+1:]

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Importing module [%s]", module_path)
        imported_module = importlib.import_module(module_path)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Instantiating class [%s]", class_name)
        new_class = getattr(imported_module, class_name)
        return new_class
