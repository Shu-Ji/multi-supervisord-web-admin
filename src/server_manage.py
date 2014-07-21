#!/usr/env/bin python2
# coding: u8

import xmlrpclib


S = dict(
    USER='nightsight',
    PASS='nightsight2',
    PORT=9002,
)
server = xmlrpclib.Server('http://%s:%s@data.corp.ganji.com:%s/RPC2' % (
    S['USER'], S['PASS'], S['PORT']))


def get_all_process_info():
    return server.supervisor.getAllProcessInfo()



if __name__ == '__main__':
    pass
