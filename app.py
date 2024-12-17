from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

contacts = {}
contact_id = 0


@app.route('/contacts', methods=['POST'])
def create_contact():
    """
    Create a new contact
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Contact'
    responses:
      201:
        description: Created
    definitions:
      Contact:
        type: object
        properties:
          name:
            type: string
          phone:
            type: string
    """
    global contact_id
    contact = request.json
    contact_id += 1
    contacts[contact_id] = contact
    return jsonify({'id': contact_id}), 201


@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """
    Get a contact by ID
    ---
    parameters:
      - name: contact_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/Contact'
      404:
        description: Not Found
    """
    if contact_id in contacts:
        return jsonify(contacts[contact_id])
    else:
        return jsonify({'error': 'Contact not found'}), 404


@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """
    Delete a contact by ID
    ---
    parameters:
      - name: contact_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: No Content
      404:
        description: Not Found
    """
    if contact_id in contacts:
        del contacts[contact_id]
        return '', 204
    else:
        return jsonify({'error': 'Contact not found'}), 404


if __name__ == '__main__':
    app.run()
