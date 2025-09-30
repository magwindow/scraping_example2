import requests
from bs4 import BeautifulSoup as Bs

url = "https://en.soccerwiki.org/league.php?leagueid=28"

html = requests.get(url).text
soup = Bs(html, "html.parser")
div = soup.find("div", class_="table-custom-responsive mb-3")
table = div.find("table", class_="table-custom table-roster")

clubs = []
for row in table.select("tr"):
    cols = row.find_all("td")
    if len(cols) >= 2:
        a = cols[1].find("a")   # вторая колонка
        if a:
            clubs.append({"name": a.get_text(strip=True), "link": a.get("href")})
# вывод
for c in clubs:
    name = c["name"]
    link = "https://en.soccerwiki.org" + c["link"]
    print(name, link)

