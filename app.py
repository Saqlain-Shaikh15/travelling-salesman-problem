from flask import Flask, render_template, request, jsonify
import itertools
import math

app = Flask(__name__)

# List of cities with their coordinates
city_list = {
    "Pune": (18.5214, 73.8567),
    "Mumbai": (19.0760, 72.8777),
    "Ahmedabad": (23.0225, 72.5714),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Delhi": (28.6139, 77.2090),
    "Jaipur": (26.9124, 75.7873),
    "Hyderabad": (17.3850, 78.4867),
    "Bangalore": (12.9716, 77.5946),
    "Lucknow": (26.8467, 80.9462)
}

@app.route('/')
def index():
    return render_template('index.html', cities=city_list.keys())

# Function to calculate the distance between two coordinates using Haversine formula
def calculate_distance(city1, city2):
    lat1, lon1 = city_list[city1]
    lat2, lon2 = city_list[city2]
    # Haversine formula to calculate the distance
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin(dlon / 2) ** 2))
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# Function to calculate the total distance of a tour
def calculate_total_distance(tour):
    total_distance = 0
    for i in range(len(tour)):
        # Adding distance from current city to the next city, and wrapping to the first city (source) after the last one
        total_distance += calculate_distance(tour[i], tour[(i + 1) % len(tour)])
    return total_distance


@app.route('/find_route', methods=['POST'])
def find_route():
    data = request.get_json()
    source = data['source']
    selected_cities = data['cities']

    # Create a list of cities including the source at the beginning
    cities_to_visit = [source] + selected_cities

    # Generate all permutations of the cities to visit
    all_tours = itertools.permutations(cities_to_visit)

    # Find the best tour with minimum distance
    best_tour = min(all_tours, key=lambda tour: calculate_total_distance(tour))

    # Append the source at the end to ensure the tour returns to the starting city
    best_tour_with_return = best_tour + (source,)

    # Calculate the total distance of the best tour
    total_distance = calculate_total_distance(best_tour_with_return)

    return jsonify({"tour": best_tour_with_return, "distance": total_distance})


if __name__ == "__main__":
    app.run(debug=True)
