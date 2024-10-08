import datetime
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

URL = "https://www.migrosbank.ch/fr/personnes-privees/prets-hypothecaires/taux-hypothecaires-actuels.html"
HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
}

SCOPE = [
	"https://spreadsheets.google.com/feeds",
	"https://www.googleapis.com/auth/spreadsheets",
	"https://www.googleapis.com/auth/drive.file",
	"https://www.googleapis.com/auth/drive"
]
FILE = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

def update(event, context):
	#fetch website
	website = None
	try:
		website = requests.get(URL, headers=HEADERS)
		website.raise_for_status()
	except requests.exceptions.ConnectionError as e:
		print("Unable to reach website server: ", str(e))
		return
	except requests.exceptions.HTTPError as e:
		print("Unable to access website: ", str(e))
		return
	if not website:
		print("Unable to retrieve website content")
		return

	#parse website
	soup = BeautifulSoup(website.text, "html.parser")
	section = soup.find(id="festhypothek-zinsen-content-0")
	if not section:
		print("Unable to find the element in the DOM")
		return

	#transform result into an array
	result = [datetime.datetime.now().replace(microsecond=0).isoformat()]
	body = section.find("tbody")
	for row in body.select("tr"):
		cells = row.select("td")
		#duration = cells[0].text
		rate = cells[1].text.replace("%", "").replace(".", ",")
		result.append(rate)

	print(result)

	credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
	client = gspread.authorize(credentials)

	sheet = client.open_by_key(FILE).sheet1
	sheet.append_row(result, value_input_option="USER_ENTERED")

if __name__ == "__main__":
	update(None, None)
