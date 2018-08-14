#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 18 - xmlrpc_server.py
# XML-RPC server
import operator, math
clients = {}
loggedClients = {}
groups = {}
addresses = {}
from SimpleXMLRPCServer import SimpleXMLRPCServer
import json

def sendRegisteredClients():
    return json.dumps(clients)

def sendLoggedClients():
    return json.dumps(loggedClients)

def sendAddresses():
    return json.dumps(addresses)

def Register(korime, lozinka, address):
    if korime in clients.keys():
        print "The username is taken"
    else:
        clients[korime] = []
        clients[korime] += [lozinka]
        addresses[korime] = json.loads(address)
    return True

def logIn(korime, lozinka, address):
    if korime in clients.keys():
        if korime in loggedClients.keys():
            print "You are already logged in"
            addresses[korime] = json.loads(address)
        else:
            loggedClients[korime] = []
            loggedClients[korime] += lozinka
    return True

def createGroup(korime, group_name):
    if korime in loggedClients.keys():
        if group_name in groups.keys():
            print "The group already exists"
        else:
            groups[group_name] = []
            groups[group_name] += korime
    else:
        print "%s is not logged in" % korime
    return True

def enterGroup(korime, group_name):
    if korime in loggedClients.keys():
        if group_name in groups:
            groups[group_name] += korime
        else:
            "The group doesn't exist"
    else:
        print "%s is not logged in"
    return True

def leaveGroup(korime, group_name):
    if korime in groups[group_name]:
        pom = groups[group_name]
        pom.remove(korime)
        groups[group_name] = pom
    return True

def logOut(korime):
    if korime in loggedClients:
        loggedClients.pop(korime)
    else:
        print "You're not logged in"
    return True

def removeFromLogged(korime):
    if korime in loggedClients.keys():
        loggedClients.pop(korime)
    else:
        print "The user is not logged in"
    return True


server = SimpleXMLRPCServer(('127.0.0.1', 7001))
server.register_introspection_functions()
server.register_multicall_functions()
server.register_function(leaveGroup)
server.register_function(createGroup)
server.register_function(Register)
server.register_function(logIn)
server.register_function(enterGroup)
server.register_function(sendAddresses)
server.register_function(sendRegisteredClients)
server.register_function(sendLoggedClients)
server.register_function(removeFromLogged)



print "Server ready"
server.serve_forever()
