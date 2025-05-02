# Zomato Restaurant Scraper

This is a Python-based scraper designed to extract structured restaurant data from Zomato URLs using a combination of HTML parsing, OCR, PDF processing, and large language models (via Cohere).

## Features

The script retrieves and processes data to output a structured JSON file with the following fields:

- restaurant_name: Name of the restaurant
- location: Full address or city/location
- operating_hours: Operating days and hours
- contact_info: Phone number, email, address, and any website or social media links
- menu_items: Up to 100 items with name, description (if available), and price
- special_features: Information on vegetarian options, spice levels, allergens, or other unique features
- reviews: Up to 10 reviews, each including:
  - star_rating (e.g., 4.5/5)
  - reviewer_name
  - comment
  - date

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/harshkalirawana/zomato_assignment.git
cd scraper

### 2. Install Python packages

- Make sure Python 3.7 or higher is installed, then run:
- pip install -r requirements.txt

### Usage
Replace your Cohere API key inside the script:
CO_API_KEY = "your_actual_api_key"

Run the script with a valid Zomato restaurant URL:
python scraper.py


## The script will:

- Scrape the /info, /order, and /reviews pages

- Detect and extract text from images and PDFs (menus)

- Use Cohere's model to format data into structured JSON

- Save the output as a JSON file in the working directory


## Output:

{
  "restaurant_name": "Super Duper Cafe",
  "location": "Technology Market, IIT Kharagpur, West Bengal, 721302",
  "operating_hours": "Monday to Sunday: 10:00 AM – 10:00 PM",
  "contact_info": {
    "phone": "+91 9876543210",
    "email": "contact@superdupercafe.in",
    "address": "Technology Market, IIT Kharagpur, West Bengal, 721302",
    "website": "https://www.superdupercafe.in",
    "social_links": [
      "https://www.instagram.com/superdupercafe",
      "https://www.facebook.com/superdupercafe"
    ]
  },
  "menu_items": [
    {
      "name": "Paneer Tikka Sandwich",
      "description": "Grilled sandwich stuffed with spicy paneer tikka, served with mint chutney.",
      "price": "₹120"
    },
    {
      "name": "Cold Coffee",
      "description": "Chilled blend of coffee, milk, and ice cream.",
      "price": "₹80"
    },
    {
      "name": "Veg Maggi",
      "description": "Masala noodles with vegetables and Indian spices.",
      "price": "₹70"
    },
    {
      "name": "French Fries",
      "description": "Crispy deep-fried potato fries served with ketchup.",
      "price": "₹90"
    },
    {
      "name": "Chilli Cheese Toast",
      "description": "Toasted bread topped with melted cheese and green chillies.",
      "price": "₹110"
    }
    // Additional items up to 100...
  ],
  "special_features": [
    "Vegetarian options available",
    "Jain-friendly dishes on request",
    "Indoor and outdoor seating",
    "Free WiFi",
    "Late-night availability"
  ],
  "reviews": [
    {
      "star_rating": "4.5/5",
      "reviewer_name": "Amit Raj",
      "comment": "Lovely place inside campus. Their cold coffee and sandwiches are a must-try!",
      "date": "2024-12-15"
    },
    {
      "star_rating": "4.0/5",
      "reviewer_name": "Sneha Paul",
      "comment": "Good food at affordable prices. Service could be a bit faster.",
      "date": "2025-01-03"
    },
    {
      "star_rating": "5.0/5",
      "reviewer_name": "Prateek Singh",
      "comment": "My go-to cafe during breaks. Paneer Tikka Sandwich is amazing.",
      "date": "2025-03-10"
    },
    {
      "star_rating": "3.5/5",
      "reviewer_name": "Neha Kumari",
      "comment": "Average taste but great ambiance. Needs more variety.",
      "date": "2025-04-01"
    },
    {
      "star_rating": "4.7/5",
      "reviewer_name": "Rahul Mehta",
      "comment": "Fast service and very tasty food. Maggi was top-notch.",
      "date": "2025-04-22"
    }
    // Additional reviews up to 10...
  ]
}
