#!/usr/bin/env python
# script will return the basic host info for ansible
import os
import sys
import argparse

try:
    import json
except:
    import simplejson as json


class Inventory(object):
    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
        if self.args.list:
            self.inventory = self.example_inventory()
        elif self.args.host:
            self.inventory = self.empty_inventory()
        else:
            self.inventory = self.empty_inventory()
        print json.dumps(self.inventory)

    def example_inventory(self):
        return {
            'group': {
                'hosts': ['192.168.2.2', '192.168.2.3'],
                'vars': {"ansible_ssh_private_key_file": "/etc/ansible/id_rsa_insecure",
                         "ansible_user": "app-admin",
                         "ansible_become": "true",
                         }
            },
            '_meta': {
                'hostvars': {
                    '192.168.2.2': {
                        'host_specific_var': 'hello'
                    },
                    '192.168.2.3': {
                        'host_specific_var': 'world'
                    }
                }
            }
        }

    def empty_inventory(self):
        return {
            '_meta': {'hostvars': {}}
        }

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


Inventory()
