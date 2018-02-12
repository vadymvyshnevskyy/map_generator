import folium
from geopy.geocoders import ArcGIS


def open_file(file):
    """
    file -> list
    Function return list of list with information about film.

    """
    a = open(file, "r")
    f = a.readlines()
    f = [w.strip().split("\t") for w in f]
    return f


def film_year(file):
    """
    file -> list
    Function return list with locations of films in order year.

    """
    year = int(input("Enter the year: "))
    place = []
    lst = open_file(file)
    for i in lst:
        for y in i:
            if "("+str(year)+")" in y:
                place.append(i[-1])
    return place


def location(place):
    """
    list -> list
    Function return list of lists with latitude and longitude of locations.
    """
    loc = []
    geolocator = ArcGIS()
    for i in place:
        try:
            location = geolocator.geocode(i)
            location1 = [location.latitude, location.longitude]
            loc.append(location1)
        except:
            pass
    return loc


def main():
    """
    This function return map with locations of films that year what you choose
    """
    map1 = folium.Map()
    lst = location(film_year("locations.list"))
    films = folium.FeatureGroup(name='Films')
    for i in lst:

        films.add_child(folium.Marker(location=i,
                                      icon=folium.Icon()))

    pop = folium.FeatureGroup(name="Population")
    pop.add_child(folium.GeoJson(data=open('world.json', 'r',
                                                  encoding='utf-8-sig').read(),
                                            style_function=lambda x: {
                                            'fillColor': 'green'
                                            if x['properties'][
                                                   'POP2005'] < 10000000
                                            else 'red' if 10000000 <=
                                                          x['properties'][
                                                        'POP2005'] < 20000000
                                            else 'black'}))
    map1.add_child(pop)
    map1.add_child(films)
    map1.add_child(folium.LayerControl())
    map1.save("Map_1.html")


main()