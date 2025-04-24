from flask import Flask, request, jsonify
from Clases.Certificate.CertificateDAO import CertificateDAO
from Clases.Certificate.Certificate import Certificate
from Clases.Error import DatabaseError

def create_certificate_routes(app):
    certificate_dao = CertificateDAO(None)  # Passing None as table_application since we're using it directly

    @app.route('/api/certificates', methods=['GET'])
    def get_all_certificates():
        try:
            certificates = certificate_dao.select_all()
            return jsonify([{
                'id': cert.id,
                'certificate_name': cert.certificate_name,
                'issuing_organization': cert.issuing_organization,
                'description': cert.description
            } for cert in certificates])
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/certificates', methods=['POST'])
    def create_certificate():
        try:
            data = request.get_json()

            # Create Certificate object from request data
            certificate = Certificate(
                certificate_name=data.get('certificate_name'),
                issuing_organization=data.get('issuing_organization'),
                description=data.get('description')
            )

            # Save certificate using DAO
            success = certificate_dao.save(certificate)

            if success:
                return jsonify({'message': 'Certificate created successfully'}), 201
            return jsonify({'error': 'Failed to create certificate'}), 400

        except (ValueError, DatabaseError) as e:
            return jsonify({'error': str(e)}), 400