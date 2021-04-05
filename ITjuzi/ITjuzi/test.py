from ITjuzi.settings import JUZI_PWD, JUZI_USER
import json


payload = {"account": JUZI_USER, "password": JUZI_PWD, "type": "pswd"}
print(type(json.dumps(payload)))
