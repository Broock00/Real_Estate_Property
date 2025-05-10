# Real Estate Property Management System

A web-based platform for managing real estate listings, customer inquiries, broker services, and admin controls. Designed for seamless interactions between **Customers**, **Brokers**, and **Admins** in a modern property management workflow.

---

## Features

### 👤 Customer
- Browse and search properties by type, price, location, and availability
- View detailed property information including images, broker contact, and map location
- Register and manage a personal profile
- Send inquiries and request property visits
- Bookmark or save favorite listings

### Broker
- Register and manage broker profiles
- Add, edit, or remove property listings
- Respond to customer inquiries
- Track listing performance (views, inquiries)
- Manage availability and pricing updates

### 👮 Admin
- Dashboard overview of users, brokers, and property listings
- Approve or reject broker registrations
- Monitor customer activity and flagged content
- Manage categories (e.g., property types, cities)
- Generate reports on platform activity


##  Tech Stack

- **Backend:** Django / Django REST Framework
- **APi's**: REST API
- **Database:** SQLite (for development)

## setup
- cd backend
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver



## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Broock00/Real_Estate_Property.git
cd Real_Estate_Property


