import requests
import traceback
import os

url = "http://isystems.hpcsa.co.za/iregister/PractitionerView.aspx?FILENO=%s"
filenos = set(el.strip() for el in open("ids.txt"))
for fileno in filenos:
    print fileno
    filename = os.path.join("detail", fileno + ".html")
    try:
        if not os.path.exists(filename):
            html = requests.get(url % fileno, timeout=25).content
            with open(filename, "w") as fp:
                fp.write(html)

    except requests.exceptions.Timeout:
        print "Timed out: %s" % fileno
    except Exception:
        traceback.print_exc()
