from bs4 import BeautifulSoup
import json
import re
import os
from glob import glob
from dateutil import parser
from datetime import datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def process_registration(soup):
    q = []
    qualifications = soup.find("table", attrs={"id" : re.compile("gvQualifications")})
    if qualifications:
        for qualification in qualifications.select("tr"):
            cells = qualification.select("td")
            if len(cells) > 0:
                q.append({
                    "degreee" : cells[0].text,
                    "date" : parser.parse(cells[1].text),
                })

    cats = []
    categories = soup.find("table", attrs={"id" : re.compile("gvCategories")})
    if categories:
        for category in categories.select("tr"):
            cells = category.select("td")
            if len(cells) > 0:
                cats.append({
                    "practice_type" : cells[0].text,
                    "practice_field" : cells[1].text,
                    "speciality" : cells[2].text,
                    "sub_speciality" : cells[3].text,
                    "from_date" : parser.parse(cells[4].text),
                    "origin" : cells[5].text,
                })

    return {
        "registration_no" : soup.find("span", attrs={"id" : re.compile("lblREGNO")}).text,
        "status" : soup.find("span", attrs={"id" : re.compile("lblREG_STS")}).text,
        "register" : soup.find("span", attrs={"id" : re.compile("lblREG_NAME")}).text,
        "board" : soup.find("span", attrs={"id" : re.compile("lblBOARD_NAME")}).text,
        "qualifications" : q,
        "categories" : cats,
    }

for filename in glob("detail/*.html"):
    if not "985009269" in filename: continue
    html = open(filename).read()
    html = html.replace("<!--", "").replace("-->", "").replace("&nbsp;", "")
    soup = BeautifulSoup(html, "html.parser")

    registrations = [
        r.parent.parent.parent.parent.parent 
        for r in soup.findAll(text=re.compile("REGISTRATION INFORMATION"))
    ]

    record = {
        "filename" : filename,
        "name" : soup.select("#ctl00_ContentPlaceHolder1_lblFullname")[0].text,
        "idno" : soup.select("#ctl00_ContentPlaceHolder1_lblId")[0].text,
        "city" : soup.select("#ctl00_ContentPlaceHolder1_lblCITY")[0].text,
        "provice" : soup.select("#ctl00_ContentPlaceHolder1_lblPROVINCE")[0].text,
        "postcode" : soup.select("#ctl00_ContentPlaceHolder1_lblPOSTAL_CODE")[0].text,
        "registrations" : [process_registration(r) for r in registrations]
    }
    print json.dumps(record, indent=4, default=json_serial)
        
