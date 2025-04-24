from flask import request, jsonify
from Clases.Grade.GradeDAO import GradeDAO
from Clases.Grade.Grade import Grade
from Clases.Error import DatabaseError

def create_grade_routes(app):
    grade_dao = GradeDAO(None)

    @app.route('/api/grades/student/<int:student_id>', methods=['GET'])
    def get_student_grades(student_id):
        try:
            grades = grade_dao.select_by_student(student_id)
            return jsonify([{
                'id': g.id,
                'grade': g.grade_value,
                'description': g.description,
                'date_of_award': g.date_of_grade,
                'course_id': g.course_id
            } for g in grades])
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/grades', methods=['POST'])
    def create_grade():
        try:
            data = request.get_json()
            grade = Grade(
                grade_value=data.get('grade_value'),
                description=data.get('description'),
                date_of_grade=data.get('date_of_grade'),
                course_id=data.get('course_id')
            )
            success = grade_dao.save(grade)
            if success:
                return jsonify({'message': 'Grade created successfully'}), 201
            return jsonify({'error': 'Failed to create grade'}), 400
        except (ValueError, DatabaseError) as e:
            return jsonify({'error': str(e)}), 400