# Premium Inventory System Starter Build

A modern, production-ready Django inventory management starter kit. Built with a focus on **premium aesthetics** without the overhead of heavy JavaScript frameworks, it leverages full-potential Vanilla CSS—making it an ideal beginner-friendly "rookie" foundation that scales flawlessly.

![Dashboard Preview](docs/dashboard-preview.png) *(Preview graphic illustrative of the UI)*

## 🌟 Key Features

- **Sleek Aesthetic UI**: Deep slate dark mode, glassmorphism cards, animated glowing gradients, and polished vector icons.
- **No JS Framework Dependency**: Pure HTML/CSS templates. Easy to learn and extend for absolute beginners.
- **Responsive Data Grids**: Custom CSS table containers for Live Stock, Logs, and Alerts that adapt perfectly to mobile and desktop screens.
- **Dynamic Items Tracking**: Supports basic properties for both `Raw Materials` (RM) and `Finished Goods` (FG) in a single unified system.
- **Production Job Cards**: Interactive module to simulate producing Finished Goods by dynamically calculating and deducting Raw Material combinations (Bill of Materials).
- **Automated Logging & Alerts**: Every transaction generates structured logs, and items falling below reorder levels are automatically flagged in an intuitive Stock Alerts dashboard.
- **Shipment Planner**: Compute spatial requirements for shipping Finished Goods using 20ft and 40ft containers based on their registered box/sack dimensions.
- **Insights & Trends**: Live business analysis tracking your inventory portfolio valuation and net production performance.

## 🛠️ Technology Stack

- **Backend Architecture**: Django (Python 3.x)
- **Database**: SQLite (default, easily swap to PostgreSQL/MySQL)
- **Frontend structure**: Django Templating Engine (`django.template`)
- **Styling**: Extensive Custom Vanilla CSS variables system

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.9+ installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/salamselu27/Inventory_System.git
   cd Inventory_System
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   *(Assuming you have a requirements.txt file, or at least Django installed)*
   ```bash
   pip install django
   ```

4. **Initialize the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **(Optional) Seed Default Data:**
   We have included a script to populate standard sample data.
   ```bash
   python seed_data.py
   ```

6. **Create an Admin User:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the local development server:**
   ```bash
   python manage.py runserver
   ```
   *Navigate to `http://127.0.0.1:8000/` to view the application.*

## 📁 Project Structure

- `inventory_system/` - Django core settings and URL routing.
- `dashboard/` - App handling the main landing pages and high-level routing.
- `inventory/` - The core application handling CRUD logic for Job Cards, Items, and Tracking.
- `balance/` - App containing business calculators, shipment planning, and financial insights dashboards.
- `customers/` - Boilerplate application ready to implement customer/supplier management.
- `static/css/theme.css` - The global design variable system driving the aesthetic UI.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Because this is structured as a starter build, simple and well-commented pull requests are vastly preferred over heavy dependencies.

## 📝 License

This project is open-source and available under the MIT License.
