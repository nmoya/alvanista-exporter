import json
import sys
from collections import defaultdict
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_html_from_url(url):
    response = urlopen(url)
    return response.read()


def clean_platform(platform):
    platform = platform.replace("-", " ")
    if platform == "ios":
        return "iOS"
    else:
        platform = platform.lower()
        tmp = []
        for word in platform.split():
            tmp.append(word[0].upper() + word[1:])
        return " ".join(tmp)


def parse_games(games, a_links):
    for tag in a_links:
        span = tag.find_all("span")
        platform = tag["href"].split("/")[2]
        platform = clean_platform(platform)
        for s in span:
            games[platform].append(s.text)


def dump_humans(games, username):
    output = []
    platforms = list(games.keys())
    for platform in sorted(platforms):
        output.append(f"{platform}\n")
        for game in sorted(games[platform]):
            output.append(f"\t- {game}")

    content = "\n".join(output)
    save(f"{username}.txt", content)
    return content


def save(filename, content):
    with open(filename, "w") as file:
        file.write(content)


def dump_json(games, username):
    content = json.dumps(games)
    save(f"{username}.json", content)
    return content


def main():
    if len(sys.argv) != 3:
        print("Call: python app.py <username> <category=finished|have|want>")
        sys.exit(-1)
    username = sys.argv[1]
    category = sys.argv[2]
    games = defaultdict(list)
    page = 1

    while True:
        url = "http://alvanista.com/%s/games/%s?page=%d" % (username, category, page)
        html = get_html_from_url(url)
        soup = BeautifulSoup(html, features="html.parser")
        all_games = soup.find_all("a", {"class": "game-cover-square game-cover-square-big"})
        if len(all_games) == 0:
            break
        else:
            parse_games(games, all_games)
            page += 1

    content = dump_humans(games, username)
    dump_json(games, username)
    print(content)


if __name__ == "__main__":
    main()
