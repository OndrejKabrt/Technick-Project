# School Management System

A comprehensive web application for managing school data including students, teachers, classes, courses, and more. The application features a responsive design with light and dark mode support.

## Features

- **Dashboard** with overview of key metrics
- **Student Management** - Add, view, and manage student records
- **Teacher Management** - Manage teacher information and assignments
- **Class Management** - Organize students into classes
- **Course Management** - Track courses and their associated subjects
- **Grade Management** - Record and view student grades
- **Certificate Management** - Track certificates issued to students
- **Student Card Management** - Manage student ID cards
- **Light/Dark Mode** - Toggle between light and dark themes
- **Responsive Design** - Works on desktop and mobile devices
- **RESTful API** - Backend API for data access

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.7 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**

   ```
   git clone https://github.com/yourusername/school-management-system.git
   cd school-management-system
   ```

2. **Install required Python packages**

   ```
   pip install flask mysql-connector-python
   ```

3. **Database Setup**

   - Create a MySQL database named `name_it_how_ever_you_like`
   - Import the database schema from the SQL file (if provided)
   - Or run the database setup script (if provided)

4. **Configure Database Connection**

   Edit the `Clases/appconfig.json` file to match your database settings:

   ```json
   {
     "database":{
       "host": "127.0.0.1",
       "port": "3306",
       "database": "bd_name",
       "user": "root",
       "password": "root"
     }
   }
   ```

   Replace the values with your actual database credentials.

## Running the Application

1. **Start the Flask application**

   ```
   python api_app.py
   ```

2. **Access the web interface**

   Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. **Using the application**

   - Navigate through the different sections using the sidebar or top navigation
   - Toggle between light and dark mode using the moon/sun icon in the top-right corner
   - Use the search functionality to find specific records
   - Add, edit, or delete records as needed

## API Documentation

The application provides a RESTful API for accessing data programmatically. You can access the API documentation at:

```
http://127.0.0.1:5000/api-docs
```

## Troubleshooting

If you encounter any issues:

1. **Database Connection Problems**
   - Verify your database credentials in `Clases/appconfig.json`
   - Ensure MySQL server is running
   - Check if the database exists and has the correct tables

2. **Application Won't Start**
   - Check if the required Python packages are installed
   - Verify that port 5000 is not in use by another application
   - Check the console output for error messages

3. **Page Loading Issues**
   - Clear your browser cache
   - Try a different browser
   - Check the browser console for JavaScript errors

## Project Structure

- `api_app.py` - Main application entry point
- `Clases/` - Core application classes
  - `DatabaseSingleton.py` - Database connection handler
  - `Student/` - Student-related classes and routes
  - `Teacher/` - Teacher-related classes and routes
  - `Class/` - Class-related classes and routes
  - `Course/` - Course-related classes and routes
  - `Subject/` - Subject-related classes and routes
  - `Grade/` - Grade-related classes and routes
  - `Certificate/` - Certificate-related classes and routes
  - `StudentCard/` - Student card-related classes and routes
- `static/` - Static assets
  - `css/` - CSS stylesheets
  - `js/` - JavaScript files
  - `img/` - Images
- `templates/` - HTML templates

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Bootstrap](https://getbootstrap.com/) - Frontend framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [MySQL](https://www.mysql.com/) - Database
