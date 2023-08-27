# Django Math Operations Tracker

Django Math Operations Tracker is a web application that allows users to perform mathematical operations by sending expressions via URLs. It provides real-time calculation results and keeps track of the last 20 operations in its history log.

## Features

- Evaluate mathematical expressions using URLs.
- View calculated results in JSON format.
- History log of the last 20 calculations.
- Persistent history log even after server restarts.

## Installation

1.Clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/django-math-operations.git
cd django-math-operations
```
2.Create a virtual environment and install the dependencies.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3.Run the development server.
```bash
python manage.py runserver
```
4. Access the app in your browser at http://localhost:8000.

## Usage

To perform a calculation, visit URLs like http://localhost:8000/5/plus/3 or http://localhost:8000/3/minus/5/plus/8.
To view the history log, go to http://localhost:8000/history.
