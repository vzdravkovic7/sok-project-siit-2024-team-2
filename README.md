# Graph Explorer

## Team
- Team Number: 2
- Members:  

  - David Stakić SV15/2022
  - Matija Šeremet SV16/2022
  - Vladimir Zdravković SV70/2022
  - Marko Cvijanović SV75/2022

---

## Project Description
Graph Explorer is a Django-based web application for creating, visualizing, and exploring interactive graphs.  
It leverages **D3.js** for visualization and **Jinja2** for templating, providing a flexible plugin system that allows easy extension of visualization features.

---

## Key Features
- Interactive graph visualization with D3.js.  
- Plugin-based architecture for extending functionality.  
- Dynamic rendering of graph data using Jinja2 templates.  
- Support for custom node and edge attributes.  
- User-friendly interface for exploring and analyzing graphs.  

---

## Architecture
- **Backend:** Django framework (Python)  
- **Frontend:** D3.js for data visualization, HTML/CSS/JS  
- **Templating:** Jinja2 for dynamic content rendering  
- **Plugins:** Modular plugin system for visualizations and data transformations  

---

## Built-in Plugins
- **Simple Visualizer Plugin** – Renders graphs using predefined D3.js layouts.  
- **Block Visualizer Plugin** – Provides block-style visualization for structured graph layouts.  
- **Datasource JSON Plugin** – Loads and parses graph data from JSON files.  
- **Datasource XML Plugin** – Loads and parses graph data from XML files.   

---

## Requirements
- Python 3.10+  
- pip (Python package manager)  
- Virtual environment (`venv`)  
- Django  
- D3.js (loaded via static files or CDN)  
- Jinja2  

---

## Installation & Setup

Clone the repository:
   ```bash
   git clone https://github.com/vzdravkovic7/sok-project-siit-2024-team-2.git
   cd <sok-project-siit-2024-team-2>
   ```

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:

Windows:

```bash
venv\Scripts\activate
```


Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```


Navigate to the Django project folder:

```bash
cd graph_explorer
```


Run the development server:

```bash
python manage.py runserver
```


Open your browser at:

```bash
http://127.0.0.1:8000/
```

## Project Configuration (Parameterization)

To successfully run the project in different environments, configure the following:

Environment variables (create a .env file or set system variables):

SECRET_KEY – Django secret key

DEBUG – set to True for local development, False for production

ALLOWED_HOSTS – list of allowed hosts (e.g., 127.0.0.1, localhost)

Database (default: SQLite, can be switched to PostgreSQL/MySQL by updating settings.py):

DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

Static and Media files configuration (if deploying in production).

## License

This project is licensed under the MIT License. See the LICENSE
 file for details.
