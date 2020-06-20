from flask import Flask, render_template
import requests 
from bs4 import BeautifulSoup 
from tabulate import tabulate 
import os 

app = Flask(__name__)

extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
url = 'https://www.mohfw.gov.in/'

#headers = ['SNo', 'State','ActiveCases', 'Cured/Discharged','Deaths', 'Total'] 

response = requests.get(url).content
soup = BeautifulSoup(response, 'html.parser')
header = extract_contents(soup.tr.find_all('th'))

stats = []
all_rows = soup.find_all('tr')

for row in all_rows:
	stat = extract_contents(row.find_all('td'))
	if stat:
		if len(stat) == 5:
			stat = ['', *stat] 
			stats.append(stat)
		elif len(stat) == 6:
			stats.append(stat)

table = stats[0:]

@app.route("/")
def home():
    return render_template("index.html", data = table)
    
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
