from flask import Flask
from werkzeug.exceptions import default_exceptions
import os
import importlib.util
import inspect

exclude_files = ['__init__.py', 'handlers.py', 'register_handlers.py']


def list_handlers():
    handlers = list()
    for file in os.listdir(os.path.dirname(__file__)):
        if file in exclude_files:
            continue
        handlers.append(file)
    return handlers


def register_handlers(app: Flask):
    founded_files = list_handlers()
    try:
        for file in founded_files:
            module_name = os.path.splitext(os.path.basename(file))[0]
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            classes_no_modulo = inspect.getmembers(module, inspect.isclass)

            for name, handler in classes_no_modulo:
                if 'Handler' in name:
                    h = handler()
                    founded_exception = list(x.get('code') == h.code for x in default_exceptions)
                    if any(x.get('code') == h.code for x in default_exceptions):
                        app.register_error_handler(h, founded_exception[0])

    except Exception as e:
        exit(500, e)
