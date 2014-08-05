from bs4 import BeautifulSoup
import urllib2
import json
import sys


def get_html_from_url(url):
	response = urllib2.urlopen(url)
	return response.read()


def clean_plataform(plataform):
	plataform = plataform.replace("-", " ")
	if plataform == "ios":
		return "iOS"
	else:
		plataform = plataform.lower()
		tmp = []
		for words in plataform.split():
			tmp.append(words[0].upper() + words[1:])
		return " ".join(tmp)

def parse_games(games, a_links):
	for tag in a_links:
	    span = tag.find_all("span")
	    plataform = tag['href'].split("/")[2]
	    plataform = clean_plataform(plataform)
	    for s in span:
	        if plataform not in games:
	        	games [plataform] = []
	        games[plataform].append(s.text)

def dump_humans(games, username):
	output = ''
	keys = games.keys()
	keys.sort()
	for plataform in keys:
		lst = games[plataform]
		lst.sort()
		output += "%s\n" % (plataform)
		for game in lst:
			output += "\t- %s\n" % (game)
		output += "\n"

	output = output.encode("utf-8")
	arq = open(username+".txt", "w")
	arq.write(output)
	arq.close()
	print output

def dump_json(games, username):
	arq = open(username+".json", "w")
	arq.write(json.dumps(games))
	arq.close()

def main():
	if len(sys.argv) != 3:
		print "Call: python app.py <username> <category=finished|have|want>"
		sys.exit(-1)
	username = sys.argv[1]
	category = sys.argv[2]
	games = {}
	page = 1

	while True:
		url = "http://alvanista.com/%s/games/%s?page=%d" % (username, category, page)
		html = get_html_from_url(url)
		soup = BeautifulSoup(html)
		agames = soup.find_all("a", {"class":"game-cover-square game-cover-square-big"})
		if len(agames) == 0:
			break
		else:
			parse_games(games, agames)
			page += 1

	dump_humans(games, username)
	dump_json(games, username)


if __name__ == "__main__":
	main()