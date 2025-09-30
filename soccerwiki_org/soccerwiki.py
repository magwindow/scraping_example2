import requests
from bs4 import BeautifulSoup as Bs

url = "https://en.soccerwiki.org/league.php?leagueid=28"

html = requests.get(url).text
soup = Bs(html, "html.parser")

print(soup.prettify())