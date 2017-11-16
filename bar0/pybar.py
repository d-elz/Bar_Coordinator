#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, argparse

from bar0.services.register_service import register_service
from bar0.services.web_register_service import web_register_service

def parse_cli():

    parser = argparse.ArgumentParser(
    prog = "Bar Coordinator", # %(prog)s : used to display the prog variable whenever you want
    usage = """%(prog)s ->"""
,
description="""
This is a bar server . Follow the commands to start the Bar Server with tcp or web

python2  bin/bar0 start server or python2  bin/bar0 start webserver
    """,

    epilog = "This is the best way to register to Bar Network",
    )

    subparsers = parser.add_subparsers(title='subcommands',
                                    description='This is the subcommands',
                                    help='additional help',
                                    dest = 'operation')

    server_parser = subparsers.add_parser('TCPserver')
    webserver_parser = subparsers.add_parser('WEBserver')

    subparsers = server_parser.add_subparsers(help='sub-command help', dest='TCPserver_operation')
    startserver_parser = subparsers.add_parser('start', help='Subparser for starting the TCP server.')

    subparsers = webserver_parser.add_subparsers(help='sub-command help', dest='WEBserver_operation')
    startwebserver_parser = subparsers.add_parser('start', help='Subparser for starting the WEB server.')

    return parser

def start_server(args):
    register_service()

def stop_server(args):
    print "stop_server"

def start_webserver(args):
    web_register_service()

def stop_webserver(args):
    print "stop_webserver"

def caller(func, args):

    return func(args)


def pybar():

    operations = {
        "TCPserver":  {
                "start" : start_server ,
                "stop" : stop_server    },
        "WEBserver":{
                "start" : start_webserver ,
                "stop" : stop_webserver    },

    }

    parser = parse_cli()
    args = parser.parse_args()
    if type(operations[args.operation]) is dict:
        caller(operations[args.operation][getattr(args, args.operation + "_operation")], args)
    else:
        caller(operations[args.operation], args)

def run():
    pybar()
