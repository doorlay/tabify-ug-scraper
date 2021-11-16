import requests, json
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from requests_html import HTMLSession

TAB_TYPE_DICT = {
        "tab": 200,
        "chord": 300
}

def build_search_url(song_name, artist_name, tab_type):
        """Builds the Search URL from the artist and song names."""
        return f"https://www.ultimate-guitar.com/search.php?title={artist_name} {song_name}&page=1&type={TAB_TYPE_DICT[tab_type]}".replace(" ", "%20")


def get_tab_page_url(search_url, tab_type):
        """Given search url, gets the url of the correct tab page."""
        resp = HTMLSession().get(search_url)
        resp.html.render(timeout=20)
        soup = BeautifulSoup(resp.html.html, "html.parser")     # Moves entire HTML file into soup
        soup = soup.find(class_="_3yi9p")                       # Cuts down to section where all tab results are listed
        soup = soup.find_all(class_="_3uKbA")                   # Splits the tab section into a list
        if soup is None:  # If no tab is found...
                return False
        for tab_link in soup:
                try:
                        if tab_link.find(class_="_2amQf _2Fdo4").text.strip() == tab_type:
                                return tab_link.find_all('a')[0].get('href')
                                break
                except:
                        pass


def scrape_tab_html(tab_page_url):
        """Given the url of the tab page, returns the HTML of the actual tab."""
        resp = HTMLSession().get(tab_page_url)
        resp.html.render(timeout=20)
        soup = BeautifulSoup(resp.html.html, "html.parser")     # Moves entire HTML file into soup
        soup = soup.find(class_="_3cXAr _1G5k-")                # Cuts down to section where all tab results are listed
        print(soup.prettify())


def get_tab(song_name, artist_name, tab_type='chords'):
        """Returns the tab for a given song.

        Args:
                song_name (string): The name of the song whose tab will be scraped.
                artist_name (string): The name of the song's artist.
                tab_type (string, optional): Either 'chords' or 'tab'. Defaults to 'chords'.

        Returns:
                string: The HTML of the tab.
        """
        search_url = build_search_url(song_name, artist_name, tab_type)
        tab_page_url = get_tab_page_url(search_url, tab_type)
        if tab_page_url == False:
                return "No Tab Found"
        return scrape_tab_html(tab_page_url)


# get_tab("Harry Styles", "Sweet Creature", "tab")
get_tab("Led Zeppelin", "Stairway to Heaven", "tab")