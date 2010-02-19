
import os
import imp
import re

def run_all(client):
    errors = []
    for name, check in _get_checkers():
        try:
            result = check.do_check(client)
            if result is not None:
                errors.append('Check "%s": %s' % (name, result))

        except AttributeError, e:
            errors.append('Invalid checker "%s": %s' % (name, e))

    return errors

def _get_checkers():
    current_dir = os.path.dirname(os.path.realpath(__file__))

    for file in os.listdir(current_dir):
        m = re.match('([a-zA-Z\d]+)\.py$', file)

        if m is not None:
            name = m.groups()[0]
            mod = imp.load_source('checker_%s' % name, os.path.join(current_dir, file))
            yield name, mod

