# zomato_assignment

Restaurant Chatbot User Interface

Overview

This project is a front-end user interface developed for a restaurant chatbot system. The interface, titled **Nugget Elegance**, is designed to provide customers with an interactive and informative platform to inquire about the restaurant's services. The application is responsive and visually appealing, built using HTML, Tailwind CSS, and JavaScript.

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
  https://github.com/harshkalirawana/zomato_assignment/tree/main/zomato
   cd restaurant-chatbot-ui
````

2. **Open the Interface**:
   Simply open `index.html` in any modern web browser.

3. **Backend Integration (Optional)**:
   Update the fetch request URL in the JavaScript section to connect with your backend service.

   Example response from backend:

   ```json
   {
     "response": "Yes, we are open from 11am to 10pm."
   }
   ```

Project Structure

```
├── index.html          # Main user interface file
└── README.md           # Project documentation
```

Notes

* The project simulates chatbot behavior for demo purposes.
* A working backend is required for dynamic responses.
* CSRF handling shown is applicable when integrated with a framework like Django.

Future Improvements

* Add persistent chat history.
* Support for images or voice-based input.
* Enhanced error handling for API failures.
* Multilingual support for broader accessibility.

License

This project is licensed under the **MIT License**. It can be used, modified, and distributed freely with attribution.

Author - Harsh Kumar

