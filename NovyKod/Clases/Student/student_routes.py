from flask import request, jsonify, render_template
from Clases.Student.StudentDAO import StudentDAO
from Clases.Student.Student import Student
from Clases.Error import DatabaseError

def create_student_routes(app):
    student_dao = StudentDAO(None)

    @app.route('/api/students/docs', methods=['GET'])
    def student_docs():
        functions = [
            {
                'method': 'GET',
                'endpoint': '/api/students',
                'description': 'Get all students'
            },
            {
                'method': 'POST',
                'endpoint': '/api/students',
                'description': 'Create a new student'
            }
        ]
        return render_template('functions.html', title='Student', functions=functions)

    @app.route('/api/students', methods=['GET'])
    def get_all_students():
        try:
            students = student_dao.select_all()
            return jsonify([{
                'id': s.id,
                'first_name': s.first_name,
                'last_name': s.last_name,
                'user_name': s.user_name,
                'number_in_class_order': s.number_in_class_order,
                'is_student': s.is_student
            } for s in students])
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/students', methods=['POST'])
    def create_student():
        try:
            data = request.get_json()
            student = Student(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                user_name=data.get('user_name'),
                user_password=data.get('user_password'),
                number_in_class_order=data.get('number_in_class_order'),
                is_student=data.get('is_student', True)
            )
            student_dao.save(student)
            return jsonify({'message': 'Student created successfully'}), 201
        except (ValueError, DatabaseError) as e:
            return jsonify({'error': str(e)}), 400
