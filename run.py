import requests
import json
import urllib, urllib2
import urlparse
from qs import _cmd, _baseheaders
from bs4 import BeautifulSoup
import re
import sys
import time

s = requests.Session()

def grab_html(url, data, headers):
    headers = headers or {}
    while True:
        try:
            data = s.post(url, data=data, headers=headers, timeout=25)
            return data
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            sys.stderr.write("Timeout: %s\n" % url)
            sys.stderr.flush()
            time.sleep(1)


url = "http://isystems.hpcsa.co.za/iregister/"
fileno_reg = re.compile("FILENO=([0-9]+)")

def print_numbers(numbers):
    for el in numbers:
        print el
    sys.stdout.flush()

def load_page1(val):
    qs = _cmd
    qs["txtId_No"] = "%%%%%%" + val + "%%%"
    r = grab_html(url, qs, _baseheaders)
    html = r.content
    ids = fileno_reg.findall(html)
    print_numbers(ids)
    return html

def load_next_page(html):
    def reached_end(html):
        if html[0] == "e":
            return True
        return False

    def extract_values(html):
        data = "|".join(html.split("|")[0:5])
        parts = html.split("|")
        run_length = parts[0]
        val_length = int(run_length)
        event_validation = data[len(run_length) + 1: len(run_length) + 1 + val_length]
        data = data[len(run_length) + 1 + val_length:]
        __gvgvResults__hidden = data

        return {
            "__EVENTVALIDATION" : event_validation,
            "__gvgvResults__hidden" : __gvgvResults__hidden
        }

    soup = BeautifulSoup(html, "html.parser")
    max_pages = int(soup.select("#lblRecordsFound")[0].text.split(":")[1].strip()) / 10

    s = "%d|0|/wFlQ7FAR9nyruIsPBAV2nNp4IseQpPNhjo44bnUJh0rIQ8=|"
    callbackparam = s + "|" + s

    qs = {
        "__EVENTTARGET" : "",
        "__EVENTARGUMENT" : "",
        "__LASTFOCUS" : "",
        "__gvgvResults__hidden" : "",
        "__VIEWSTATE" : soup.select("#__VIEWSTATE")[0]["value"],
        "__EVENTVALIDATION" : soup.select("#__EVENTVALIDATION")[0]["value"],
        "SearchChkb$3" : "on",
        "txtId_No" : soup.select("#txtId_No")[0]["value"],
        "rgId_No" : "rbIdnoWildcard",
        "__CALLBACKID" : "gvResults",
        "__CALLBACKPARAM" : callbackparam % (1, 0),
    }

    for i in range(1, max_pages + 1):
        try:
            r = grab_html(url, qs, _baseheaders)
            html = r.content
            if "Runtime Error" in html: 
                print "Runtime Error: ID: " + soup.select("#txtId_No")[0]["value"], "page: " + str(i)
            ids = fileno_reg.findall(html)
            print_numbers(ids)
            if reached_end(html):
                break
            values = extract_values(html)
            values["__CALLBACKPARAM"] = callbackparam % (i + 1, i)
            qs.update(values)
        except ValueError:
            import traceback; traceback.print_exc()

def load_position():
    with open("position.dat") as fp:
        try:
            return int(fp.read())
        except TypeError:
            return 0

def mark_position(i):
    with open("position.dat", "w") as fp:
        fp.write(str(i))

def cycle():
    for i in range(load_position(), 10000):
        mark_position(i)
        val = str(i).zfill(4)
        sys.stderr.write("\r%s" % val)
        html = load_page1(val)
        load_next_page(html)

cycle()
#load_next_page(open("out.html").read())


