import json
import ssl
import urllib.error
import urllib.request

import folium
import twurl
from folium.plugins import FloatImage
from opencage.geocoder import OpenCageGeocode

key = ''
geocoder = OpenCageGeocode(key)


def read_data(acct):
    """Returns the friends of the given Twitter user.

    Parameters:
        acct (str): Twitter username

    Returns:
        (list): a list with first element being the given username and others
        being the information about his friends in the (name, screen_name,
        location, profile_image_url) format
    """
    twitter_url = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = twurl.augment(twitter_url, {'screen_name': acct, 'count': '42'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)

    return [acct] + [(user['name'], user['screen_name'], user['location'],
                      user['profile_image_url']) for user in js['users'] if
                     user['location'] != []]


def create_map(data: list) -> None:
    """Creates a map of the given user's friends."""
    my_map = folium.Map(location=(0, 0), zoom_start=2)

    username = data[0]

    # Creates markers of the given user's friends
    fg_f = folium.FeatureGroup(name=f"Friends of {username}")
    for name, screen_name, location, profile_image_url in data[1:]:
        try:
            results = geocoder.geocode(location)[0]['geometry']
            value = f"<b>Name:</b> {name}\n<b>Twitter:</b> @{screen_name}"
            fg_f.add_child(
                folium.Marker(location=(results['lat'], results['lng']),
                              popup=value,
                              icon=folium.features.CustomIcon(
                                  profile_image_url, icon_size=(25, 25))))
        except:
            continue

    my_map.add_child(fg_f)
    my_map.add_child(FloatImage('https://i.imgur.com/SV6rA7f.png', bottom=5,
                                left=90, ))
    my_map.add_child(folium.LayerControl())

    # Saves map
    my_map.save('templates/map.html')
