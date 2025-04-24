from flask import request, jsonify
from Clases.Subject.SubjectDAO import SubjectDAO
from Clases.Subject.Subject import Subject
from Clases.Error import DatabaseError

def create_subject_routes(app):
    subject_dao = SubjectDAO(None)

    @app.route('/api/subjects', methods=['GET'])
    def get_all_subjects():
        try:
            subjects = subject_dao.select_all()
            return jsonify([{
                'id': s.id,
                'subject_name': s.subject_name,
                'subject_description': s.subject_description
            } for s in subjects])
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/subjects', methods=['POST'])
    def create_subject():
        try:
            data = request.get_json()
            subject = Subject(
                subject_name=data.get('subject_name'),
                subject_description=data.get('subject_description')
            )
            success = subject_dao.save(subject)
            if success:
                return jsonify({'message': 'Subject created successfully'}), 201
            return jsonify({'error': 'Failed to create subject'}), 400
        except (ValueError, DatabaseError) as e:
            return jsonify({'error': str(e)}), 400