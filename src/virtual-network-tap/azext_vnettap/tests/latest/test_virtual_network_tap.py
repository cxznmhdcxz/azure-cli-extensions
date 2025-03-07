# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

import os
import unittest
from azure.cli.testsdk import *
import json


class VirtualNetworkTAPScenarioTest(ScenarioTest):

    @ResourceGroupPreparer(name_prefix= 'cli_test_vnet_tap_', location='eastus2', random_name_length=40)
    def test_vnet_tap(self, resource_group):

        self.kwargs.update({
            'vnet1': 'vnet1',
            'subnet1': 'subnet1',
            'lb': 'lb',
            'source_nic': 'sourcenic',
            'nic': 'destnic',
            'nic_ipconfig': 'nicipconfig1',
            'tap1': 'tap1',
            'tap2': 'tap2',
            'vtap_config1': 'vtapconfig1',
            'vtap_config2': 'vtapconfig2'
        })
        self.cmd('network vnet create -g {rg} -n {vnet1} --subnet-name {subnet1}')
        self.cmd('network nic create -g {rg} -n {source_nic} --subnet {subnet1} --vnet-name {vnet1} --accelerated-networking true --auxiliary-mode AcceleratedConnections --auxiliary-sku A1', checks=[
                  self.check('NewNIC.auxiliaryMode', 'AcceleratedConnections'),
                  self.check('NewNIC.auxiliarySku', 'A1')
                ])

        # case: create vtap with nic destination
        self.cmd('network nic create -g {rg} -n {nic} --subnet {subnet1} --vnet-name {vnet1} ')
        self.cmd('network nic ip-config create -g {rg} --nic-name {nic} --name {nic_ipconfig}')
        self.kwargs['nic_dest'] = self.cmd('network nic ip-config show -g {rg} --nic-name {nic} --name {nic_ipconfig}').get_output_in_json()['id']
        self.cmd('network vnet tap create -g {rg} -n {tap1} --destination {nic_dest}', checks=[
                  self.check('type', 'Microsoft.Network/virtualNetworkTaps'),
                  self.check('destinationNetworkInterfaceIPConfiguration.id', self.kwargs['nic_dest'])
                ])
        # create vtap config
        self.cmd('network nic vtap-config create -g {rg} -n {vtap_config1} --nic {source_nic} --vnet-tap {tap1}', checks=[
                  self.check('type', 'Microsoft.Network/networkInterfaces/tapConfigurations'),
                  self.check('name', self.kwargs['vtap_config1'])
                ])
        self.cmd('network nic vtap-config delete -g {rg} -n {vtap_config1} --nic {source_nic} -y')

        # case: create vtap with lb destination
        self.cmd('network lb create -g {rg} -n {lb}  --sku Standard --subnet {subnet1} --vnet-name {vnet1}')
        self.kwargs['lb_dest'] = self.cmd('network lb frontend-ip show -g {rg} --lb-name {lb} --name LoadBalancerFrontEnd').get_output_in_json()['id']
        self.cmd('network vnet tap create -g {rg} -n {tap2} --destination {lb_dest}', checks=[
                  self.check('type', 'Microsoft.Network/virtualNetworkTaps'),
                  self.check('name', self.kwargs['tap2'])
                ])
        self.cmd('network nic vtap-config create -g {rg} -n {vtap_config2} --nic {source_nic} --vnet-tap {tap2}')
        self.cmd('network nic vtap-config delete -g {rg} -n {vtap_config2} --nic {source_nic} -y')
