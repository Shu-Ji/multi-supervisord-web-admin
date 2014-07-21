# coding: u8

import xmlrpclib


def get_one_host_info(host):
    server = xmlrpclib.Server('http://%(user)s:%(pwd)s@%(host)s:%(port)s/RPC2'
            % host.as_dict())
    return server.supervisor.getAllProcessInfo()
