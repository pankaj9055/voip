# VoipFit Website - replit.md

## Overview

VoipFit is a Flask-based web application for a VoIP service provider. The system consists of a public-facing website showcasing services and company information, along with a comprehensive admin panel for content management. The application features a modern, responsive design with dynamic content management capabilities.

## System Architecture

The application follows a traditional Flask MVC architecture with the following key components:

### Frontend Architecture
- **Public Website**: Bootstrap 5 + custom CSS with responsive design
- **Admin Panel**: Separate admin interface with custom styling
- **Template Engine**: Jinja2 templates with inheritance
- **Static Assets**: CSS, JavaScript, and uploaded images served from static directory

### Backend Architecture
- **Framework**: Flask with Blueprint-based routing
- **Database ORM**: SQLAlchemy with declarative base
- **Authentication**: Flask-Login for admin sessions
- **Email Integration**: Flask-Mail for contact form submissions
- **File Uploads**: Werkzeug secure filename handling

### Data Storage
- **Primary Database**: SQLite (configurable via DATABASE_URL)
- **File Storage**: Local filesystem for uploaded images
- **Session Storage**: Flask sessions with configurable secret key

## Key Components

### Database Models
- **Admin**: User authentication and management
- **Content**: Dynamic content management with section/key structure
- **CarouselImage**: Homepage carousel image management
- **ContactMessage**: Contact form submissions with read status

### Route Blueprints
- **main_bp** (`routes.py`): Public website routes (home, about, services, contact)
- **admin_bp** (`admin_routes.py`): Admin panel routes with authentication required

### Content Management System
- Section-based content organization (home, about, services, contact)
- Key-value pairs for flexible content storage
- Support for text, HTML, and image URL content types
- Dynamic content retrieval via `get_content()` helper function

### Authentication System
- Password hashing using Werkzeug security functions
- Session-based authentication with Flask-Login
- Admin-only access to management features

## Data Flow

1. **Public Website**: Templates retrieve dynamic content via `get_content()` function from Content model
2. **Contact Forms**: Submissions stored in ContactMessage model and optionally emailed
3. **Admin Panel**: CRUD operations on all models with authentication checks
4. **Image Management**: File uploads with secure filename handling and database tracking

## External Dependencies

### Python Packages
- Flask (web framework)
- SQLAlchemy (database ORM)
- Flask-Login (authentication)
- Flask-Mail (email functionality)
- Werkzeug (utilities and security)

### Frontend Libraries
- Bootstrap 5.3.0 (UI framework)
- Font Awesome 6.0.0 (icons)
- Google Fonts (Inter typography)

### Services
- SMTP server for email functionality (configurable)
- File system for image storage

## Deployment Strategy

The application is designed for flexible deployment with:

### Configuration Management
- Environment variables for sensitive data (DATABASE_URL, MAIL_* settings)
- Fallback defaults for development
- ProxyFix middleware for reverse proxy deployments

### Database Setup
- SQLAlchemy with engine options for connection pooling
- Database URL configuration via environment variable
- Support for SQLite (default) and PostgreSQL

### File Handling
- Configurable upload directory
- 16MB file size limit
- Secure filename processing

### Production Considerations
- Session secret key via environment variable
- Mail server configuration for contact forms
- Static file serving (should be handled by web server in production)

## Changelog

```
Changelog:
- June 30, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```