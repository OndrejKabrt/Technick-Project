from flask import request, jsonify
from Clases.StudentCard.StudentCardDAO import StudentCardDAO
from Clases.StudentCard.StudentCard import StudentCard
from Clases.Error import DatabaseError

def create_student_card_routes(app):
    student_card_dao = StudentCardDAO(None)

    @app.route('/api/student-cards/<int:student_id>', methods=['GET'])
    def get_student_card(student_id):
        try:
            card = student_card_dao.find_by_student_id(student_id)
            if card:
                return jsonify({
                    'id': card.id,
                    'town': card.town,
                    'street': card.street,
                    'descriptive_number': card.descriptive_number,
                    'zip_code': card.zip_code,
                    'email': card.email,
                    'date_of_birth': card.date_of_birth,
                    'phone_number': card.phone_number,
                    'student_id': card.student_id
                })
            return jsonify({'error': 'Student card not found'}), 404
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/student-cards', methods=['POST'])
    def create_student_card():
        try:
            data = request.get_json()
            card = StudentCard(
                town=data.get('town'),
                street=data.get('street'),
                descriptive_number=data.get('descriptive_number'),
                zip_code=data.get('zip_code'),
                email=data.get('email'),
                date_of_birth=data.get('date_of_birth'),
                phone_number=data.get('phone_number'),
                student_id=data.get('student_id')
            )
            success = student_card_dao.save(card)
            if success:
                return jsonify({'message': 'Student card created successfully'}), 201
            return jsonify({'error': 'Failed to create student card'}), 400
        except (ValueError, DatabaseError) as e:
            return jsonify({'error': str(e)}), 400