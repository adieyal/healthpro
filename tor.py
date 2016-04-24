"""
setup:
pip install requesocks
super helpful:
http://packetforger.wordpress.com/2013/08/27/pythons-requests-module-with-socks-support-requesocks/
    """
import requests
import socket
import socks
import sys

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050, True, 'socks5_user','socks_pass')
socket.socket = socks.socksocket

html = requests.get("http://check.torproject.org").content
if "Congratulations" in html:
    sys.stderr.write("Connected to TOR\n")
else:
    sys.stderr.write("Not connected to TOR\n")
   
    sys.exit()
