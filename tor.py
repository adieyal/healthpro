"""
setup:
pip install requesocks
super helpful:
http://packetforger.wordpress.com/2013/08/27/pythons-requests-module-with-socks-support-requesocks/
    """
import requests
import socket
import socks

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050, True, 'socks5_user','socks_pass')
socket.socket = socks.socksocket

print requests.get("http://check.torproject.org").content
