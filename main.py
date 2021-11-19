import requests, json
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
app = Flask(__name__)


def build_chord(chord):
        return f'<span class="_3PpPJ OrSDI" data-name="{chord}" style="color: rgb(0, 0, 0);">{chord}</span>'


def get_chord_type(unparsed_html, index):
        characters_in_chord = 10
        chord_type = unparsed_html[index+4]
        index = index + 5
        while unparsed_html[index] != "[":
                chord_type += unparsed_html[index]
                characters_in_chord += 1
                index += 1
        return chord_type, characters_in_chord


def char_is_chord(unparsed_html, index):
        return unparsed_html[index:index+4] == "[ch]"


def parse_tab_page(unparsed_html):
        tab_html = '<section class="_3cXAr _1G5k-"><code class="_3enQP"><pre class="_3F2CP _3hukP" style="font-size: 13px; font-family: Roboto Mono, Courier New, monospace;"><span class="_3rlxz">'
        i = 0
        while i < len(unparsed_html):
                # If carriage return ...
                if unparsed_html[i:i+2] == "\r":
                        i += 2
                # If newline ...
                elif unparsed_html[i:i+2] == "\n":
                        tab_html += "\n"
                        i += 2
                # Below statements are added to skip the tab tags
                elif unparsed_html[i:i+6] == "[/tab]":
                        i += 6
                elif unparsed_html[i:i+5] == "[tab]":
                        i += 5
                # If the next section is a chord ... 
                elif char_is_chord(unparsed_html, i):
                        chord_type, chars = get_chord_type(unparsed_html, i)
                        tab_html += build_chord(chord_type)
                        i += chars
                # If character isn't special, add it normally
                else:
                        tab_html += unparsed_html[i]
                        i += 1
        tab_html += "</section>"
        return tab_html
        

def build_search_url(song_name, artist_name):
        """Builds the Search URL from the artist and song names."""
        return f"https://www.ultimate-guitar.com/search.php?title={artist_name} {song_name}&page=1&type=300".replace(" ", "%20")


def get_tab_page_url(search_url):
        """Given search url, gets the url of the correct tab page."""
        resp = requests.get(search_url)
        soup = BeautifulSoup(resp.content, "html.parser")
        soup = soup.find(class_="js-store")
        page_data = json.loads(soup["data-content"])
        results = page_data["store"]["page"]["data"]["results"]
        for tab in results:
                if "type" in tab.keys() and tab["type"] == "Chords":
                        return tab["tab_url"]
        return False


def scrape_tab_html(tab_page_url):
        """Given the url of the tab page, returns the HTML of the actual tab."""
        resp = requests.get(tab_page_url)
        soup = BeautifulSoup(resp.content, "html.parser")
        soup = soup.find(class_="js-store")              
        page_data = json.loads(soup["data-content"])
        unparsed_html = page_data["store"]["page"]["data"]["tab_view"]["wiki_tab"]["content"]
        return parse_tab_page(unparsed_html)


def get_tab(song_name, artist_name):
        """Returns the tab for a given song.

        Args:
                song_name (string): The name of the song whose tab will be scraped.
                artist_name (string): The name of the song's artist.

        Returns:
                string: The HTML of the tab.
        """
        search_url = build_search_url(song_name, artist_name)
        tab_page_url = get_tab_page_url(search_url)
        if tab_page_url == False:
                return False

        return scrape_tab_html(tab_page_url)


@app.route('/gettab/', methods=['GET'])
def respond():
        # Retrieve the name from url parameter
        artist_name = request.args.get("artist_name", None)
        song_name = request.args.get("song_name", None)

        response = {}

        # If artist_name is not included
        if not artist_name:
                response["ERROR"] = "artist name not included."
        # If song_name is not included
        elif not song_name:
                response["ERROR"] = "song name not included."
        # When a valid request is made
        else:
                tab = get_tab(artist_name, song_name)
                if tab == False:
                        response["ERROR"] = "no tab found."
                else:
                        response["TAB"] = tab

        # Return the response in json format
        return jsonify(response)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(port=5000)

"""
EXAMPLE CALLS:

Make a GET request with the following: http://127.0.0.1:5000/gettab?artist_name=Harry Styles&song_name=Sweet Creature

"""
