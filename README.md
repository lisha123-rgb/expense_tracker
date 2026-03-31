# expense_tracker
💰 Expense Tracker Web Application

A production-ready full-stack web application that enables users to securely track, categorize, and analyze their expenses.
Built with a focus on backend architecture, database design, and deployment practices.

🚀 Live Demo
🔗 https://web-production-9aa88.up.railway.app

🧩 Problem Statement
Managing daily expenses manually is inefficient and lacks insights.
This application solves that by providing:
1. Structured expense tracking
2. Automatic categorization
3. Visual analytics for spending patterns

⚙️ Tech Stack
Backend:
1. Flask
2. Flask-SQLAlchemy
3. Flask-Login
4. Flask-WTF

Frontend:
1. HTML5
2. Bootstrap 5
3. Bootstrap Icons
4. Chart.js

Database:
1. PostgreSQL (Production)
2. SQLite (Development)

Deployment:
1. Railway
2. Gunicorn

✨ Features
🔐 Authentication & Security: 
User registration and login
Password hashing using werkzeug.security
CSRF protection (Flask-WTF)
Secure session management
POST-only sensitive operations
💰 Expense Management:
Add, view, and delete expenses
User-specific data isolation
Latest-first sorting
Clean and responsive UI
🧠 Intelligent Categorization:
Rule-based keyword detection system
Automatically assigns categories like:
Food
Travel
Shopping
Bills
Entertainment
📊 Analytics Dashboard: 
Category-wise expense breakdown
Interactive pie chart (Chart.js)
Month & year filtering
Handles empty datasets gracefully
📱 Responsive Design: 
Mobile-first UI using Bootstrap
Table layout (desktop)
Card layout (mobile)

🏗 System Architecture
Client (Browser)
      ↓
Flask Application (Routes + Logic)
      ↓
SQLAlchemy ORM
      ↓
PostgreSQL Database

🗃 Database Schema
User
id
username
email
password_hash
Category
id
name
Expense
id
amount
description
date
category_id (FK)
user_id (FK)

Relationships: 
One User → Many Expenses
One Category → Many Expenses

🔐 Security Practices
Password hashing (no plain-text storage)
CSRF protection on all forms
Secure session handling (HTTPOnly cookies)
Restricted HTTP methods for critical actions

🚀 Deployment
Hosted on Railway
Uses PostgreSQL cloud database
Production server: Gunicorn

📌 Key Learning Outcomes
Built a full-stack Flask application
Designed relational database schemas
Implemented secure authentication systems
Integrated frontend with backend APIs
Deployed production-ready app with cloud database

📈 Future Improvements
Expense editing
Budget alerts
CSV/PDF export
REST API support
Docker containerization

⭐ Acknowledgment
This project was developed as part of hands-on learning in full-stack web development and deployment.