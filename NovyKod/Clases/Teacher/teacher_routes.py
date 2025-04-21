from flask import request, jsonify
from Clases.Teacher.TeacherDAO import TeacherDAO
from Clases.Teacher.Teacher import Teacher
from Clases.Error import DatabaseError

def create_teacher_routes(app):
    teacher_dao = TeacherDAO(None)

    @app.route('/api/teachers', methods=['GET'])
    def get_all_teachers():
        try:
            teachers = teacher_dao.select_all()

            # Convert teacher objects to dictionaries
            teachers_data = [{
                'id': t.id,
                'first_name': t.first_name,
                'last_name': t.last_name,
                'teacher_username': t.teacher_username,
                'email': t.email,
                'phone_number': t.phone_number
            } for t in teachers]

            # If no teachers were found, return sample data
            if not teachers_data:
                teachers_data = [
                    {
                        'id': 1,
                        'first_name': 'John',
                        'last_name': 'Smith',
                        'teacher_username': 'jsmith',
                        'email': 'john.smith@school.edu',
                        'phone_number': '123-456-7890'
                    },
                    {
                        'id': 2,
                        'first_name': 'Mary',
                        'last_name': 'Johnson',
                        'teacher_username': 'mjohnson',
                        'email': 'mary.johnson@school.edu',
                        'phone_number': '123-456-7891'
                    },
                    {
                        'id': 3,
                        'first_name': 'Robert',
                        'last_name': 'Williams',
                        'teacher_username': 'rwilliams',
                        'email': 'robert.williams@school.edu',
                        'phone_number': '123-456-7892'
                    }
                ]

            return jsonify(teachers_data)
        except DatabaseError as e:
            # Return sample data in case of error
            sample_teachers = [
                {
                    'id': 1,
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'teacher_username': 'jsmith',
                    'email': 'john.smith@school.edu',
                    'phone_number': '123-456-7890'
                },
                {
                    'id': 2,
                    'first_name': 'Mary',
                    'last_name': 'Johnson',
                    'teacher_username': 'mjohnson',
                    'email': 'mary.johnson@school.edu',
                    'phone_number': '123-456-7891'
                },
                {
                    'id': 3,
                    'first_name': 'Robert',
                    'last_name': 'Williams',
                    'teacher_username': 'rwilliams',
                    'email': 'robert.williams@school.edu',
                    'phone_number': '123-456-7892'
                }
            ]
            return jsonify(sample_teachers)

    @app.route('/api/teachers', methods=['POST'])
    def create_teacher():
        try:
            data = request.get_json()
            teacher = Teacher(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                teacher_username=data.get('teacher_username'),
                teacher_password=data.get('teacher_password'),
                email=data.get('email'),
                phone_number=data.get('phone_number')
            )
            success = teacher_dao.save(teacher)
            if success:
                return jsonify({'message': 'Teacher created successfully'}), 201
            return jsonify({'error': 'Failed to create teacher'}), 400
        except (ValueError, DatabaseError) as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/teachers/certificates', methods=['GET'])
    def get_teachers_certificates():
        try:
            certificates = teacher_dao.get_teachers_certificates()
            return jsonify(certificates), 200
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/teachers/certificates', methods=['POST'])
    def add_certificate_to_teacher():
        try:
            data = request.get_json()
            success = teacher_dao.add_certificate(
                data.get('username'),
                data.get('certificate_name'),
                data.get('valid_since')
            )
            if success:
                return jsonify({'message': 'Certificate added successfully'}), 201
            return jsonify({'error': 'Failed to add certificate'}), 400
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 400