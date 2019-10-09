# -*- coding: utf-8 -*-
'''
Test States
===========

Provide test case states that enable easy testing of things to do with state
calls, e.g. running, calling, logging, output filtering etc.

.. code-block:: yaml

    always-passes-with-any-kwarg:
      test.nop:
        - name: foo
        - something: else
        - foo: bar

    always-passes:
      test.succeed_without_changes:
        - name: foo

    always-fails:
      test.fail_without_changes:
        - name: foo

    always-changes-and-succeeds:
      test.succeed_with_changes:
        - name: foo

    always-changes-and-fails:
      test.fail_with_changes:
        - name: foo
'''
# Import Python libs
import random


def nop(hub, name, **kwargs):
    '''
    A no-op state that does nothing. Useful in conjunction with the `use`
    requisite, or in templates which could otherwise be empty due to jinja
    rendering
    '''
    return succeed_without_changes(hub, name)


def succeed_without_changes(hub, name, **kwargs):
    '''
    name
        A unique string.
    '''
    ret = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': 'Success!'
    }
    return ret


def fail_without_changes(hub, name, **kwargs):
    '''
    Returns failure.

    name:
        A unique string.
    '''
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': 'Failure!'
    }

    return ret


def succeed_with_changes(hub, name, **kwargs):
    '''
    Returns successful and changes is not empty

    name:
        A unique string.
    '''
    ret = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': 'Success!'
    }

    ret['changes'] = {
        'testing': {
            'old': 'Unchanged',
            'new': 'Something pretended to change'
        }
    }

    return ret


def fail_with_changes(hub, name, **kwargs):
    '''
    Returns failure and changes is not empty.

    name:
        A unique string.
    '''
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': 'Failure!'
    }
    ret['changes'] = {
        'testing': {
            'old': 'Unchanged',
            'new': 'Something pretended to change'
        }
    }
    return ret


def update_low(hub, name, __run_name):
    '''
    Use the __run_name to add a run to the low
    '''
    extra = {
        '__sls__': 'none',
        'name': 'totally_extra_alls',
        '__id__': 'king_arthur',
        'state': 'test',
        'fun': 'nop'}
    hub.idem.RUNS[__run_name]['low'].append(extra)
    return succeed_without_changes(hub, name)


def mod_watch(hub, name, **kwargs):
    '''
    Return a mod_watch call for test
    '''
    ret = {
        'name': name,
        'changes': {'watch': True},
        'result': True,
        'comment': 'Watch ran!'
    }
    return ret
