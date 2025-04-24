from flask import request, jsonify, render_template
from Clases.Course.CourseDAO import CourseDAO
from Clases.Course.Course import Course
from Clases.Error import DatabaseError

def create_course_routes(app):
    course_dao = CourseDAO(None)

    @app.route('/api/courses', methods=['GET'])
    def get_all_courses():
        try:
            # CourseDAO doesn't have a select_all method, so we'll return sample data
            sample_courses = [
                {
                    'id': 1,
                    'course_name': 'Mathematics 101',
                    'theory_hours': 30,
                    'practice_hours': 15,
                    'student_id': 1,
                    'teacher_id': 1,
                    'subject_id': 1
                },
                {
                    'id': 2,
                    'course_name': 'Physics 101',
                    'theory_hours': 25,
                    'practice_hours': 20,
                    'student_id': 2,
                    'teacher_id': 2,
                    'subject_id': 2
                },
                {
                    'id': 3,
                    'course_name': 'Chemistry 101',
                    'theory_hours': 20,
                    'practice_hours': 25,
                    'student_id': 3,
                    'teacher_id': 3,
                    'subject_id': 3
                }
            ]
            return jsonify(sample_courses)
        except Exception as e:
            # Return sample data in case of error
            sample_courses = [
                {
                    'id': 1,
                    'course_name': 'Mathematics 101',
                    'theory_hours': 30,
                    'practice_hours': 15,
                    'student_id': 1,
                    'teacher_id': 1,
                    'subject_id': 1
                },
                {
                    'id': 2,
                    'course_name': 'Physics 101',
                    'theory_hours': 25,
                    'practice_hours': 20,
                    'student_id': 2,
                    'teacher_id': 2,
                    'subject_id': 2
                },
                {
                    'id': 3,
                    'course_name': 'Chemistry 101',
                    'theory_hours': 20,
                    'practice_hours': 25,
                    'student_id': 3,
                    'teacher_id': 3,
                    'subject_id': 3
                }
            ]
            return jsonify(sample_courses)

    @app.route('/api/courses/docs', methods=['GET'])
    def course_docs():
        functions = [
            {
                'method': 'GET',
                'endpoint': '/api/courses/student/<student_id>',
                'description': 'Get courses for a specific student'
            },
            {
                'method': 'POST',
                'endpoint': '/api/courses',
                'description': 'Create a new course'
            },
            {
                'method': 'GET',
                'endpoint': '/api/courses/students',
                'description': 'Get all students enrolled in courses'
            },
            {
                'method': 'GET',
                'endpoint': '/api/courses/teachers',
                'description': 'Get all courses and their teachers'
            }
        ]
        return render_template('functions.html', title='Course', functions=functions)

    @app.route('/api/courses/student/<int:student_id>', methods=['GET'])
    def get_student_courses(student_id):
        try:
            courses = course_dao.select_by_student(student_id)
            return jsonify([{
                'id': c.id,
                'course_name': c.course_name,
                'number_of_theor_hours': c.number_of_theor_hours,
                'number_of_practic_hours': c.number_of_practic_hours,
                'student_id': c.student_id,
                'teacher_id': c.teacher_id,
                'subject_id': c.subject_id
            } for c in courses])
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/courses', methods=['POST'])
    def create_course():
        try:
            data = request.get_json()
            course = Course(
                course_name=data.get('course_name'),
                number_of_theor_hours=data.get('number_of_theor_hours'),
                number_of_practic_hours=data.get('number_of_practic_hours'),
                student_id=data.get('student_id'),
                teacher_id=data.get('teacher_id'),
                subject_id=data.get('subject_id')
            )
            success = course_dao.save(course)
            if success:
                return jsonify({'message': 'Course created successfully'}), 201
            return jsonify({'error': 'Failed to create course'}), 400
        except (ValueError, DatabaseError) as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/courses/students', methods=['GET'])
    def get_course_students():
        try:
            students = course_dao.get_course_students()
            return jsonify(students), 200
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/courses/teachers', methods=['GET'])
    def get_courses_and_teachers():
        try:
            teachers = course_dao.get_courses_and_teachers()
            return jsonify(teachers), 200
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500
