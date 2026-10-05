"""
StayType AI - NYC Airbnb Neighborhoods & Presets Data Mapping
"""

BOROUGH_NEIGHBORHOOD_MAP = {
    "Manhattan": [
        "Battery Park City", "Chelsea", "Chinatown", "Civic Center", "East Harlem",
        "East Village", "Financial District", "Flatiron District", "Gramercy",
        "Greenwich Village", "Harlem", "Hell's Kitchen", "Inwood", "Kips Bay",
        "Little Italy", "Lower East Side", "Marble Hill", "Midtown", "Morningside Heights",
        "Murray Hill", "NoHo", "Nolita", "Roosevelt Island", "SoHo", "Stuyvesant Town",
        "Theater District", "Tribeca", "Two Bridges", "Upper East Side", "Upper West Side",
        "Washington Heights", "West Village"
    ],
    "Brooklyn": [
        "Bath Beach", "Bay Ridge", "Bedford-Stuyvesant", "Bensonhurst", "Bergen Beach",
        "Boerum Hill", "Borough Park", "Brighton Beach", "Brooklyn Heights", "Brownsville",
        "Bushwick", "Canarsie", "Carroll Gardens", "Clinton Hill", "Cobble Hill",
        "Columbia St", "Coney Island", "Crown Heights", "Cypress Hills", "DUMBO",
        "Downtown Brooklyn", "Dyker Heights", "East Flatbush", "East New York", "Flatbush",
        "Flatlands", "Fort Greene", "Fort Hamilton", "Gowanus", "Gravesend", "Greenpoint",
        "Kensington", "Manhattan Beach", "Midwood", "Mill Basin", "Navy Yard",
        "Park Slope", "Prospect Heights", "Prospect-Lefferts Gardens", "Red Hook",
        "Sea Gate", "Sheepshead Bay", "South Slope", "Sunset Park", "Vinegar Hill",
        "Williamsburg", "Windsor Terrace"
    ],
    "Queens": [
        "Arverne", "Astoria", "Bay Terrace", "Bayside", "Bayswater", "Belle Harbor",
        "Bellerose", "Breezy Point", "Briarwood", "Cambria Heights", "College Point",
        "Corona", "Ditmars Steinway", "Douglaston", "East Elmhurst", "Edgemere",
        "Elmhurst", "Far Rockaway", "Flushing", "Forest Hills", "Fresh Meadows",
        "Glendale", "Hollis", "Holliswood", "Howard Beach", "Jackson Heights",
        "Jamaica", "Jamaica Estates", "Jamaica Hills", "Kew Gardens", "Kew Gardens Hills",
        "Laurelton", "Little Neck", "Long Island City", "Maspeth", "Middle Village",
        "Neponsit", "Ozone Park", "Queens Village", "Rego Park", "Richmond Hill",
        "Ridgewood", "Rockaway Beach", "Rosedale", "South Ozone Park", "Springfield Gardens",
        "St. Albans", "Sunnyside", "Whitestone", "Woodhaven", "Woodside"
    ],
    "Bronx": [
        "Allerton", "Baychester", "Belmont", "Bronxdale", "Castle Hill", "City Island",
        "Claremont Village", "Clason Point", "Co-op City", "Concourse", "Concourse Village",
        "East Morrisania", "Eastchester", "Edenwald", "Fieldston", "Fordham",
        "Highbridge", "Hunts Point", "Kingsbridge", "Longwood", "Melrose",
        "Morris Heights", "Morris Park", "Morrisania", "Mott Haven", "Mount Eden",
        "Mount Hope", "North Riverdale", "Norwood", "Olinville", "Parkchester",
        "Pelham Bay", "Pelham Gardens", "Port Morris", "Riverdale", "Schuylerville",
        "Soundview", "Spuyten Duyvil", "Throgs Neck", "Tremont", "Unionport",
        "University Heights", "Van Nest", "Wakefield", "West Farms", "Westchester Square",
        "Williamsbridge", "Woodlawn"
    ],
    "Staten Island": [
        "Arden Heights", "Arrochar", "Bay Terrace, Staten Island", "Bull's Head",
        "Castleton Corners", "Clifton", "Concord", "Dongan Hills", "Eltingville",
        "Emerson Hill", "Graniteville", "Grant City", "Great Kills", "Grymes Hill",
        "Howland Hook", "Huguenot", "Mariners Harbor", "Midland Beach", "New Brighton",
        "New Dorp", "New Dorp Beach", "New Springville", "Oakwood", "Port Richmond",
        "Prince's Bay", "Randall Manor", "Rosebank", "Rossville",
        "Shore Acres", "Silver Lake", "South Beach", "St. George", "Stapleton",
        "Todt Hill", "Tompkinsville", "Tottenville", "West Brighton", "Westerleigh",
        "Willowbrook"
    ]
}

BOROUGH_DEFAULT_COORDS = {
    "Manhattan": {"latitude": 40.7831, "longitude": -73.9712},
    "Brooklyn": {"latitude": 40.6782, "longitude": -73.9442},
    "Queens": {"latitude": 40.7282, "longitude": -73.7949},
    "Bronx": {"latitude": 40.8448, "longitude": -73.8648},
    "Staten Island": {"latitude": 40.5795, "longitude": -74.1502}
}

PRESET_LISTINGS = [
    {
        "id": "manhattan-luxury",
        "name": "Midtown Manhattan Luxury Loft",
        "badge": "Entire Home",
        "icon": "fa-building",
        "data": {
            "neighbourhood_group": "Manhattan",
            "neighbourhood": "Midtown",
            "latitude": 40.7549,
            "longitude": -73.9840,
            "price": 350.0,
            "minimum_nights": 3,
            "number_of_reviews": 48,
            "reviews_per_month": 2.15,
            "calculated_host_listings_count": 2,
            "availability_365": 240
        }
    },
    {
        "id": "brooklyn-private",
        "name": "Williamsburg Bohemian Suite",
        "badge": "Private Room",
        "icon": "fa-bed",
        "data": {
            "neighbourhood_group": "Brooklyn",
            "neighbourhood": "Williamsburg",
            "latitude": 40.7081,
            "longitude": -73.9571,
            "price": 85.0,
            "minimum_nights": 2,
            "number_of_reviews": 65,
            "reviews_per_month": 3.40,
            "calculated_host_listings_count": 1,
            "availability_365": 120
        }
    },
    {
        "id": "queens-shared",
        "name": "Flushing Traveler Shared Pod",
        "badge": "Shared Room",
        "icon": "fa-people-roof",
        "data": {
            "neighbourhood_group": "Queens",
            "neighbourhood": "Flushing",
            "latitude": 40.7580,
            "longitude": -73.8290,
            "price": 35.0,
            "minimum_nights": 1,
            "number_of_reviews": 112,
            "reviews_per_month": 4.80,
            "calculated_host_listings_count": 5,
            "availability_365": 350
        }
    },
    {
        "id": "soho-penthouse",
        "name": "SoHo Designer Penthouse",
        "badge": "Entire Home",
        "icon": "fa-gem",
        "data": {
            "neighbourhood_group": "Manhattan",
            "neighbourhood": "SoHo",
            "latitude": 40.7233,
            "longitude": -74.0030,
            "price": 490.0,
            "minimum_nights": 4,
            "number_of_reviews": 29,
            "reviews_per_month": 1.45,
            "calculated_host_listings_count": 1,
            "availability_365": 180
        }
    }
]

STAY_TYPE_DETAILS = {
    "Entire home/apt": {
        "title": "Entire Home / Apartment",
        "icon": "fa-house-chimney",
        "color": "emerald",
        "bg_class": "bg-emerald-500/10 border-emerald-500/30 text-emerald-400",
        "description": "Guests have the whole place to themselves. Includes a private bedroom, bathroom, living space, and kitchen.",
        "best_for": "Couples, families, executives, and travelers seeking maximum privacy."
    },
    "Private room": {
        "title": "Private Room",
        "icon": "fa-bed",
        "color": "sky",
        "bg_class": "bg-sky-500/10 border-sky-500/30 text-sky-400",
        "description": "Guests have their own private bedroom for sleeping. Other areas (kitchen, living room, bathroom) may be shared.",
        "best_for": "Solo travelers, students, budget tourists seeking privacy without paying full apartment rates."
    },
    "Shared room": {
        "title": "Shared Room",
        "icon": "fa-people-roof",
        "color": "amber",
        "bg_class": "bg-amber-500/10 border-amber-500/30 text-amber-400",
        "description": "Guests sleep in a bedroom or common area that is shared with others, typically hostel-style or bunk bed setups.",
        "best_for": "Backpackers, ultra-budget travelers, and nomadic short-term crashers."
    }
}
