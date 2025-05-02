# zomato_assignment

Restaurant Chatbot User Interface

Overview

This project is a front-end user interface developed for a restaurant chatbot system. The interface, titled **Nugget Elegance**, is designed to provide customers with an interactive and informative platform to inquire about the restaurant's services. The application is visually appealing, built using HTML, Tailwind CSS, and JavaScript.

Objectives

- To deliver an intuitive chat experience for restaurant visitors.
- To simulate a real-time conversation with a virtual assistant.
- To offer seamless integration with a server-side application for dynamic replies.

Features

- Responsive Design: Optimized for various screen sizes including desktops, tablets, and mobile phones.
- Predefined Questions: Users can quickly choose from commonly asked questions.
- Modern UI Styling: Implements Tailwind CSS and glassmorphism for an elegant design.
- Interactive Chat Flow: Users can type and submit queries, with dynamic bot replies displayed in a conversational format.
- Backend-Ready Structure: The interface includes fetch functionality to connect with a RESTful backend endpoint.

Technologies Used

- **HTML5** – Markup for structure
- **Tailwind CSS** – Styling and layout
- **Vanilla JavaScript** – For DOM manipulation and handling user input
- **Optional Backend** – Expects an endpoint that returns responses in JSON format

Installation and Usage

1. **Clone the Repository**:
   ```bash
  https://github.com/harshkalirawana/zomato_assignment.git
   cd chatbot
````

2. **Open the Interface**:
   Simply open `chat.html`(/chat) in any modern web browser.

3. **Backend Integration (Optional)**:
   Update the fetch request URL in the JavaScript section to connect with your backend service.

   Example response from backend:

   ```json
   {
     "response": "Yes, we are open from 11am to 10pm."
   }
   ```

### Project Structure:

ZOMATO_ASSIGNMENT/
├── chatbot/
│ ├── templates/
│ │ └── chatbot/
│ │ └── chat.html
│ ├── zomato/
│ │ ├── pycache/
│ │ ├── data/
│ │ ├── server/
│ │ │ ├── pycache/
│ │ │ └── main.py
│ │ ├── init.py
│ │ ├── asgi.py
│ │ ├── settings.py
│ │ ├── urls.py
│ │ ├── views.py
│ │ ├── wsgi.py
│ │ ├── db.sqlite3
│ │ └── manage.py
│ └── requirements.txt
├── scraper/
│ ├── restaurants_data/
│ ├── requirements.txt
│ ├── scraper_readme.md
│ └── scraper.py
└── README.md

### Install Python packages

- Make sure Python 3.7 or higher is installed, then run:
- pip install -r requirements.txt

### Save Hugging Face token (replace if needed)

HfFolder.save_token('token')

### Notes

* The project simulates chatbot behavior for demo purposes.
* A working backend is required for dynamic responses.
* CSRF handling shown is applicable when integrated with a framework like Django.

### Future Improvements

* Add persistent chat history.
* Support for images or voice-based input.
* Enhanced error handling for API failures.
* Multilingual support for broader accessibility.

License

This project is licensed under the **MIT License**. It can be used, modified, and distributed freely with attribution.

Author - Harsh Kumar

