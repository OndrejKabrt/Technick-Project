from flask import Flask, render_template, jsonify, request, send_from_directory
import logging
import os
from Clases.Certificate.certificate_routes import create_certificate_routes
from Clases.Class.class_routes import create_class_routes
from Clases.Course.course_routes import create_course_routes
from Clases.Grade.grade_routes import create_grade_routes
from Clases.Student.student_routes import create_student_routes
from Clases.StudentCard.student_card_routes import create_student_card_routes
from Clases.Subject.subject_routes import create_subject_routes
from Clases.Teacher.teacher_routes import create_teacher_routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['DEBUG'] = True

# Register all API routes
create_certificate_routes(app)
create_class_routes(app)
create_course_routes(app)
create_grade_routes(app)
create_student_routes(app)
create_student_card_routes(app)
create_subject_routes(app)
create_teacher_routes(app)

# Web interface routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/students')
def students_page():
    return render_template('students.html')

@app.route('/classes')
def classes_page():
    return render_template('classes.html')

@app.route('/teachers')
def teachers_page():
    return render_template('teachers.html')

@app.route('/courses')
def courses_page():
    return render_template('courses.html')

@app.route('/subjects')
def subjects_page():
    return render_template('subjects.html')

@app.route('/grades')
def grades_page():
    return render_template('grades.html')

@app.route('/certificates')
def certificates_page():
    return render_template('certificates.html')

@app.route('/student-cards')
def student_cards_page():
    return render_template('student_cards.html')

# API Documentation routes
@app.route('/api/docs')
def api_docs():
    docs = [
        {'name': 'Students', 'url': '/api/students/docs'},
        {'name': 'Classes', 'url': '/api/classes/docs'},
        {'name': 'Teachers', 'url': '/api/teachers/docs'},
        {'name': 'Courses', 'url': '/api/courses/docs'},
        {'name': 'Subjects', 'url': '/api/subjects/docs'},
        {'name': 'Grades', 'url': '/api/grades/docs'},
        {'name': 'Certificates', 'url': '/api/certificates/docs'},
        {'name': 'Student Cards', 'url': '/api/student-cards/docs'}
    ]
    return render_template('api_docs.html', docs=docs)

# Additional API routes for the dashboard
@app.route('/api/grades', methods=['GET'])
def get_all_grades():
    try:
        # This is a placeholder - in a real app, you would fetch from a database
        # For now, we'll return sample data for demonstration
        sample_grades = [
            {
                'id': 1,
                'student_id': 1,
                'student_name': 'John Doe',
                'course_id': 1,
                'course_name': 'Mathematics',
                'grade_value': 5,
                'date_of_grade': '2023-05-15',
                'description': 'Final exam'
            },
            {
                'id': 2,
                'student_id': 2,
                'student_name': 'Jane Smith',
                'course_id': 2,
                'course_name': 'Physics',
                'grade_value': 4,
                'date_of_grade': '2023-05-20',
                'description': 'Midterm exam'
            },
            {
                'id': 3,
                'student_id': 3,
                'student_name': 'Mike Johnson',
                'course_id': 3,
                'course_name': 'Chemistry',
                'grade_value': 3,
                'date_of_grade': '2023-05-25',
                'description': 'Lab work'
            }
        ]
        return jsonify(sample_grades)
    except Exception as e:
        logger.error(f'Error fetching grades: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/grades', methods=['POST'])
def add_grade():
    try:
        data = request.json
        # In a real app, you would save this to a database
        # For now, we'll just return success
        return jsonify({'success': True, 'message': 'Grade added successfully', 'id': 4}), 201
    except Exception as e:
        logger.error(f'Error adding grade: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/grades/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    try:
        # In a real app, you would delete from a database
        # For now, we'll just return success
        return jsonify({'success': True, 'message': f'Grade {grade_id} deleted successfully'})
    except Exception as e:
        logger.error(f'Error deleting grade: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/student-cards', methods=['GET'])
def get_all_student_cards():
    try:
        # For student cards, we'll use the students data and generate card info
        from Clases.Student.StudentDAO import StudentDAO
        student_dao = StudentDAO(None)
        students = student_dao.select_all()

        # Generate student cards data
        student_cards = []
        for student in students:
            # Generate a card number based on student ID
            card_number = f"SC-{student.id:03d}-{2023}"

            # Generate issue and expiry dates
            from datetime import datetime, timedelta
            issue_date = datetime.now().strftime('%Y-%m-%d')
            expiry_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')

            # Create a card with a unique ID (different from student ID)
            # In a real app, this would be a separate entity in the database
            card_id = int(f"{student.id}001")  # Create a unique card ID based on student ID

            student_cards.append({
                'id': card_id,  # Unique card ID
                'student_id': student.id,  # Reference to the student
                'student_name': f"{student.first_name} {student.last_name}",
                'card_number': card_number,
                'issue_date': issue_date,
                'expiry_date': expiry_date,
                'active': True
            })

        return jsonify(student_cards)
    except Exception as e:
        logger.error(f'Error fetching student cards: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/student-cards/<int:card_id>', methods=['GET'])
def get_student_card_by_id(card_id):
    try:
        # In a real app, you would fetch the card from a database
        # For now, we'll generate it on the fly

        # Extract student ID from card ID (assuming card_id format is student_id + 001)
        student_id = card_id // 1000

        from Clases.Student.StudentDAO import StudentDAO
        student_dao = StudentDAO(None)
        student = student_dao.find_by_id(student_id)

        if not student:
            return jsonify({'error': 'Student card not found'}), 404

        # Generate card data
        card_number = f"SC-{student.id:03d}-{2023}"

        from datetime import datetime, timedelta
        issue_date = datetime.now().strftime('%Y-%m-%d')
        expiry_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')

        card = {
            'id': card_id,
            'student_id': student.id,
            'student_name': f"{student.first_name} {student.last_name}",
            'card_number': card_number,
            'issue_date': issue_date,
            'expiry_date': expiry_date,
            'active': True
        }

        return jsonify(card)
    except Exception as e:
        logger.error(f'Error fetching student card: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>/card', methods=['GET'])
def get_student_card_by_student_id(student_id):
    try:
        # In a real app, you would fetch the card from a database
        # For now, we'll generate it on the fly
        from Clases.Student.StudentDAO import StudentDAO
        student_dao = StudentDAO(None)
        student = student_dao.find_by_id(student_id)

        if not student:
            return jsonify({'error': 'Student not found'}), 404

        # Generate card data
        card_id = int(f"{student.id}001")  # Create a unique card ID based on student ID
        card_number = f"SC-{student.id:03d}-{2023}"

        from datetime import datetime, timedelta
        issue_date = datetime.now().strftime('%Y-%m-%d')
        expiry_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')

        card = {
            'id': card_id,
            'student_id': student.id,
            'student_name': f"{student.first_name} {student.last_name}",
            'card_number': card_number,
            'issue_date': issue_date,
            'expiry_date': expiry_date,
            'active': True
        }

        return jsonify(card)
    except Exception as e:
        logger.error(f'Error fetching student card: {str(e)}')
        return jsonify({'error': str(e)}), 500

# Certificate route is already defined in the certificate_routes.py file

@app.route('/api/classes/<int:class_id>', methods=['GET'])
def get_class(class_id):
    try:
        # In a real app, you would fetch from a database
        # For demo purposes, we'll return mock data
        from Clases.Class.ClassDAO import ClassDAO
        class_dao = ClassDAO(None)
        class_obj = class_dao.find_by_id(class_id)

        if class_obj:
            return jsonify({
                'id': class_obj.id,
                'name': class_obj.name,
                'grade': class_obj.grade,
                'number_of_class': class_obj.number_of_class,
                'year_of_entry': class_obj.year_of_entry,
                'active': class_obj.active,
                'class_teacher_id': class_obj.class_teacher_id
            })
        return jsonify({'error': 'Class not found'}), 404
    except Exception as e:
        logger.error(f'Error fetching class: {str(e)}')
        return jsonify({'error': str(e)}), 500



@app.route('/api/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    try:
        from Clases.Teacher.TeacherDAO import TeacherDAO
        teacher_dao = TeacherDAO(None)
        teacher = teacher_dao.find_by_id(teacher_id)

        if teacher:
            return jsonify({
                'id': teacher.id,
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
                'teacher_username': teacher.teacher_username,
                'email': teacher.email,
                'phone_number': teacher.phone_number
            })
        return jsonify({'error': 'Teacher not found'}), 404
    except Exception as e:
        logger.error(f'Error fetching teacher: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/teachers/<int:teacher_id>/classes', methods=['GET'])
def get_teacher_classes(teacher_id):
    try:
        # In a real app, you would fetch from a database
        # For now, we'll return sample data
        if teacher_id == 1:
            return jsonify([{'id': 1, 'name': 'Class 5A'}])
        return jsonify([])
    except Exception as e:
        logger.error(f'Error fetching teacher classes: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/teachers/<int:teacher_id>/subjects', methods=['GET'])
def get_teacher_subjects(teacher_id):
    try:
        # In a real app, you would fetch from a database
        # For now, we'll return sample data
        if teacher_id == 1:
            return jsonify([{'id': 1, 'name': 'Mathematics'}, {'id': 2, 'name': 'Physics'}])
        return jsonify([])
    except Exception as e:
        logger.error(f'Error fetching teacher subjects: {str(e)}')
        return jsonify({'error': str(e)}), 500



@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        from Clases.Course.CourseDAO import CourseDAO
        course_dao = CourseDAO(None)
        course = course_dao.find_by_id(course_id)

        if course:
            return jsonify({
                'id': course.id,
                'course_name': course.course_name,
                'theory_hours': course.theory_hours,
                'practice_hours': course.practice_hours,
                'student_id': course.student_id,
                'teacher_id': course.teacher_id,
                'subject_id': course.subject_id
            })
        return jsonify({'error': 'Course not found'}), 404
    except Exception as e:
        logger.error(f'Error fetching course: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
