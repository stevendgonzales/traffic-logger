from bs4 import BeautifulSoup
import requests

from traffic_logging.data.utils import parse_traffic_event


def get_traffic_events():
    """
    scrape the City of San Antonio traffic data website and parse the text
    into traffic events
    """
    #make a web request for the traffic data web site
    response = requests.get('https://webapps2.sanantonio.gov/traffic/Traffic.aspx')
    html_text = response.text

    #turn the html text form the requested site into a beautiful soup object
    #and parse out the grid related to traffic data
    soup = BeautifulSoup(html_text)
    grid_outer = soup.find(id="GridView1")
    grid_inner = grid_outer.find_all("tr")

    #create a list of TrafficEvent objects from the data
    # retrieved from the web request
    traffic_events = [parse_traffic_event(row.find_all("td"))
                      for row in grid_inner if len(row.find_all("td")) > 4]

    return traffic_events
