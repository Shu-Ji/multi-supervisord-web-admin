# coding: u8

import xmlrpclib


def _gen_server(host):
    if host.user:
        return xmlrpclib.Server('http://%(user)s:%(pwd)s@%(host)s:%(port)s/RPC2'
                % host.as_dict())
    else:
        return xmlrpclib.Server('http://%(host)s:%(port)s/RPC2'
                % host.as_dict())


def get_one_host_info(host):
    return _gen_server(host).supervisor.getAllProcessInfo()


def restart_one_process(host, name, group):
    sv = _gen_server(host).supervisor
    name = ':'.join([group, name])
    try:
        sv.stopProcess(name)
    except:
        pass
    sv.startProcess(name)


def stop_one_process(host, name, group):
    sv = _gen_server(host).supervisor
    name = ':'.join([group, name])
    try:
        sv.stopProcess(name)
    except:
        pass
