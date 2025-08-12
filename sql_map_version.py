import folium
import webbrowser
from geopy.distance import geodesic

def show_locations_on_map(location1_name, latitude1, longitude1, location2_name, latitude2, longitude2):
    # Create a folium map centered around the average of the specified coordinates
    avg_latitude = (latitude1 + latitude2) / 2
    avg_longitude = (longitude1 + longitude2) / 2
    map_location = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=12)

    # Add markers for the first location
    folium.Marker(
        location=[latitude1, longitude1],
        popup=location1_name,
        icon=folium.Icon(color='red')
    ).add_to(map_location)

    # Add markers for the second location
    folium.Marker(
        location=[latitude2, longitude2],
        popup=location2_name,
        icon=folium.Icon(color='blue')
    ).add_to(map_location)

    # Add a line connecting the two locations
    folium.PolyLine(locations=([latitude1, longitude1], [latitude2, longitude2]), color='green').add_to(map_location)

    # Calculate and display the distance between the two locations
    distance_km = round(geodesic((latitude1, longitude1), (latitude2, longitude2)).kilometers, 2)
    distance_text = f"Distance: {distance_km} km"
    folium.Marker(
        location=[avg_latitude, avg_longitude],
        popup=distance_text,
        icon=folium.Icon(color='purple')
    ).add_to(map_location)

    # Save the map to a temporary HTML file
    temp_html_file = f'{location1_name}_{location2_name}_map_temp.html'
    map_location.save(temp_html_file)

    # Open the HTML file in the default web browser
    webbrowser.open(temp_html_file)

# Example: Coordinates for Liverpool and Manchester
liverpool_latitude = 53.4084
liverpool_longitude = -2.9916

manchester_latitude = 53.4839
manchester_longitude = -2.2446

# Show Liverpool and Manchester on the same map with a connecting line and distance
show_locations_on_map('Liverpool', liverpool_latitude, liverpool_longitude, 'Manchester', manchester_latitude, manchester_longitude)