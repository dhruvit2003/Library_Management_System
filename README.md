# Library Management System

This is a simple Library Management System built using Django Rest Framwork. It's bulit on Test-Driven Development (TDD) process. It allows users to perform operation like adding books, borrowing books, returning books, and viewing available books. Here to store a data used JSON file insted of Database.

## Getting Started

### Prerequisites

- Python 3.x
- Django 3.x or later
- Django REST Framework

### Installation

1. *Clone the repository:*
    - git clone https://github.com/yourusername/Library_Management_System.git
    - cd Library_Management_System

2. *Create and activate a virtual environment:*
    - python -m venv venv
    - venv\Scripts\activate   (On Linux: source venv/bin/activate)

3. *Install the required packages:*
    - pip install -r requirements.txt
    
4. *Run the Django development server:*
    - cd Library_Management_System
    - python manage.py runserver

### Running the Tests

To run all the tests, use the following command:
- python manage.py test
