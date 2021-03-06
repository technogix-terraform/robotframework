""" -----------------------------------------------------
# TECHNOGIX
# -------------------------------------------------------
# Copyright (c) [2022] Technogix SARL
# All rights reserved
# -------------------------------------------------------
# Keywords to manage ec2 tasks
# -------------------------------------------------------
# Nadège LEMPERIERE, @05 october 2021
# Latest revision: 05 october 2021
# --------------------------------------------------- """

# System includes
from sys import path as syspath
from os import path
from json import dumps

# Robotframework includes
from robot.api import logger
ROBOT = False

# Local include
syspath.append(path.normpath(path.join(path.dirname(__file__), './')))
from tool import Tool

class EC2Tools(Tool) :
    """ Class providing tools to check AWS codecommit compliance """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.m_services.append('ec2')

    def is_ebs_encryption_activated(self) :
        """ Test if encryption is activated on EC2 instances disks """

        result = False
        if self.m_is_active['ec2'] :
            response = self.m_clients['ec2'].get_ebs_encryption_by_default()
            if response['EbsEncryptionByDefault'] is True : result = True

        return result

    def subnet_exists(self, subnet) :
        """ Test if a subnet exists in a VPC
            ---
            subnet    (str) : Subnet to look for in the VPC
        """

        result = False

        subnets = self.list_subnets()
        for sub in subnets :
            for tag in sub['Tags'] :
                if tag['Key'] == 'Name' and tag['Value'] == subnet : result = True

        return result

    def nacl_exists(self, nacl) :
        """ Test if a nacl exists in a VPC
            ---
            nacl    (str) : Access control list to look for in the VPC
        """

        result = False

        nacls = self.list_network_acls()
        for acl in nacls :
            for tag in acl['Tags'] :
                logger.info(dumps(tag))
                if tag['Key'] == 'Name' and tag['Value'] == nacl : result = True

        return result

    def list_regions(self) :
        """ List all activated regions """

        result = []
        if self.m_is_active['ec2'] :
            response = self.m_clients['ec2'].describe_regions()
            result = response['Regions']

        return result

    def list_vpcs(self) :
        """ List existing vpcs  """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_vpcs')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['Vpcs']

        return result

    def list_subnets(self) :
        """ List existing subnets  """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_subnets')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['Subnets']

        return result

# pylint: disable=W0102
    def list_images(self, owners=[]) :
        """ List existing instance images """

        result = []
        if self.m_is_active['ec2'] :
            response = self.m_clients['ec2'].describe_images(Owners=owners)
            result = response['Images']

        return result
# pylint: enable=W0102

    def list_flow_logs(self) :
        """ List existing flow logs """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_flow_logs')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['FlowLogs']

        return result

    def list_instances(self) :
        """ List existing instances """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_instances')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                for reservation in response['Reservations'] :
                    result = result + reservation['Instances']

        return result

    def list_volumes(self) :
        """ List existing ebs volumes  """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_volumes')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['Volumes']

        return result

    def list_network_interfaces(self) :
        """ List existing network interfaces """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_network_interfaces')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['NetworkInterfaces']

        return result


    def list_network_acls(self) :
        """ List network access control lists """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_network_acls')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['NetworkAcls']

        return result

    def list_vpc_default_security_groups(self) :
        """ List vpc default security groups"""

        result = []

        sgs = self.list_vpc_security_groups()
        for sgroup in sgs :
            logger.info(dumps(sgroup))
            if sgroup['GroupName'] == "default" :
                result.append(sgroup)

        return result

    def list_vpc_security_groups(self) :
        """ List vpc security groups """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_security_groups')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['SecurityGroups']

        return result

    def list_security_groups_rules(self) :
        """ List all security groups rules """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_security_group_rules')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['SecurityGroupRules']

        return result

    def list_route_tables(self) :
        """ List route tables """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_route_tables')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['RouteTables']

        return result

    def list_internet_gateways(self) :
        """ List all internet gateways """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_internet_gateways')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                for gateway in response['InternetGateways'] :
                    gateway['EgressOnly'] = False
                    result.append(gateway)

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator(\
                'describe_egress_only_internet_gateways')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                for gateway in response['EgressOnlyInternetGateways'] :
                    gateway['EgressOnly'] = True
                    gateway['InternetGatewayId'] = gateway['EgressOnlyInternetGatewayId']
                    del gateway['EgressOnlyInternetGatewayId']
                    result.append(gateway)

        return result

    def list_vpc_endpoints(self) :
        """ List vpc service endpoints """

        result = []

        if self.m_is_active['ec2'] :
            paginator = self.m_clients['ec2'].get_paginator('describe_vpc_endpoints')
            response_iterator = paginator.paginate()
            for response in response_iterator :
                result = result + response['VpcEndpoints']

        return result


# pylint: disable=R0201, R1716
    def nacl_allow_remote_administration_access(self, entry) :
        """ Check if an access control list entry allow administration access
            ---
            entry    (dict) : Entry to analyze
        """
        result = False

        port_range_allow_admin = ( \
            not 'PortRange' in entry or \
            (   entry['PortRange']['From'] <= 22 and \
                entry['PortRange']['To'] >= 22) or \
            (   entry['PortRange']['From'] <= 3389 and \
                entry['PortRange']['To'] >= 3389))
        logger.info(entry)
        if  not entry['Egress'] and \
            entry['RuleAction'] == 'allow' and \
            entry['CidrBlock'] == '0.0.0.0/0' and \
            port_range_allow_admin :
            result = True

        return result


    def rule_allow_remote_administration_access(self, entry) :
        """ Check if a security group allow administration access """

        result = False

        port_range_allow_admin = ( \
            not 'ToPort' in entry or \
            entry['IpProtocol'] == '-1' or \
            entry['IpProtocol'] == 'all' or \
            (   isinstance(entry['ToPort'], int) and \
                entry['ToPort'] == 22) or \
            (   isinstance(entry['ToPort'], str) and \
                (entry['ToPort'].split("-")[0].strip() <= 22 and \
                entry['ToPort'].split("-")[1].strip() >= 22)) or \
            (   isinstance(entry['ToPort'], int) and \
                entry['ToPort'] == 3389) or \
            (   isinstance(entry['ToPort'], str) and \
                (entry['ToPort'].split("-")[0].strip() <= 3389 and \
                entry['ToPort'].split("-")[1].strip() >= 3389)))
        source_allow_external = ( \
            ('CidrIpv4' in entry and entry['CidrIpv4'] == '0.0.0.0/0') or \
            ('CidrIpv6' in entry and entry['CidrIpv6'] == '::0')
        )

        logger.info(entry)
        if not entry['IsEgress'] and source_allow_external and port_range_allow_admin :
            result = True

        return result
# pylint: enable=R0201, R1716
