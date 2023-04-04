from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from db.connect import get_data_robots
import requests
import urllib3
import json

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

insert = get_data_robots()

#Get data from apis
headers = {"Authorization": "jwt:eyJraWQiOiJTRU5BQyIsImFsZyI6IlJTMjU2In0.eyJpc3MiOiJTRU5BQy1QT1JUQUwtRUFEIiwiYXVkIjoiQ01TX1BPUlRBTF9FQURfQVBQIiwiZXhwIjoxNjgwNTczMTM4LCJqdGkiOiJOMkFSZVRlMHgwT25XZm9URmROU3dnIiwiaWF0IjoxNjgwNTI5OTM4LCJuYmYiOjE2ODA1Mjk4MTgsInN1YiI6IlVzZXIiLCJkYXRhIjoie1wiaWRcIjo5LFwidXN1YXJpb1wiOlwiZnJvbnRlbmQtcG9ydGFsXCIsXCJhcGxpY2FjYW9cIjpcIlBPUlRBTC1FQURcIn0ifQ.TknC9_AOCZ74cCn5aq-wpPcrK2UbpMaXrE-XddtpHvPfNpKWI9gBnKJZpBsl9rKr8x6JofggIUPx8I6GlYwY5kIqZrTHT04tMcP7yVoVKOiNpyIxPQNMopGyWU0HmhEM1-xYWUjO92_CSoQWN1KqyZkz9OIE7XA86uDiotpOekvNGJF-T0ttgmvQJZtYRM7hvO3qoroXJ_kqDyE40DlXTQptjkM_wW7-JvtBZA6wXm-9SGbe8kzlRQgFHKjRZHYDZ3YqvYU18LYr6ALeCGvis4T5DFCMWZlvPbMEHL2L1VeeNJFMbBzWH3uxkJsrNfrw4HRN6TqbWU39hdKbPfQ8cw"}
get_courses = requests.get("https://www.ead.senac.br/cms/api/areas/buscar-por-path-modalidade/graduacao?instant-request=1680543430065", headers=headers,verify=False)
courses = get_courses.json()

get_ufs = requests.get("https://www.ead.senac.br/cms/api/ufs?instant-request=1680543430065", headers=headers, verify=False)
ufs = get_ufs.json()

list_ufs = []
for uf in ufs:
    uf_data = {
        "name": uf["nome"],
        "sigla": uf["sigla"]
    }
    list_uf = list_ufs.append(uf_data)

list_courses = []
for cc in courses:
    for cn in cc["cursos"]:
        data_course = {
            "name": cn["titulo"],
            "path": cn["path"],
            "id": str(cn["id"])
        }
        list_course = list_courses.append(data_course)

for lc in list_courses:
    for lu in list_ufs:
        get_payment_ids = requests.get("https://www.ead.senac.br/cms/api/turmas/forma-pagamento-curso/"+lc["path"]+"?instant-request=1680545579812", headers=headers, verify=False)
        payment_ids = get_payment_ids.json()

        for payment_id in payment_ids:
            get_locals = requests.get("https://www.ead.senac.br/cms/api/turmas/turma-departamento-uf-ativos/"+lc["id"]+"/"+lu["sigla"]+"?instant-request=1680545589159", headers=headers, verify=False)
            localss = get_locals.json()

            for locall in localss:
                data_local = {
                    "name": locall["nome"],
                    "id": str(locall["id"])
                }

            get_prices = requests.get("https://www.ead.senac.br/cms/api/turmas/precoespecial/"+lu["sigla"]+"/"+data_local["id"]+"/"+str(payment_id["id"])+"?instant-request=1680545589159", headers=headers, verify=False)
            print("https://www.ead.senac.br/cms/api/turmas/precoespecial/"+lu["sigla"]+"/"+data_local["id"]+"/"+lc["id"]+"?instant-request=1680545630887")
            prices = get_prices.json()

            for price in prices:
                insert.insert_scrap_data(
                    ies_name="SENAC",
                    course_name=lc["name"],
                    uf_name=lu["name"],
                    local_name=data_local["name"],
                    price=str(price["valorParcela"]),
                    full_price=str(price["valorTotal"])
                )