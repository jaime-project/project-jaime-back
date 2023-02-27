import ntpath
from io import BytesIO

import yaml
from flask import Blueprint, jsonify, request, send_file

from logic.apps.messages import service
from logic.apps.messages.model import Message, Status

blue_print = Blueprint('messages', __name__, url_prefix='/api/v1/messages')


@blue_print.route('/', methods=['POST'])
def post():
    s = request.json
    m = Message(
        title=s['title'],
        subject=s['subject'],
        body=s['body'],
        job=s['job'],
        files=s.get('files', []),
    )
    service.add(m)
    return m.id, 201


@ blue_print.route('/<id>', methods=['GET'])
def get(id: str):
    s = service.get(id)
    if not s:
        return '', 204

    return jsonify(s.__dict__()), 200


@ blue_print.route('/', methods=['GET'])
def list_all():
    return jsonify(service.list_all()), 200


@ blue_print.route('/status', methods=['GET'])
def list_status():
    return jsonify(service.list_status()), 200


@ blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):
    service.delete(id)
    return '', 200


@ blue_print.route('/all/short', methods=['GET'])
def get_all_short():

    size = int(request.args.get('size', 3))
    page = int(request.args.get('page', 1))
    filter = request.args.get('filter', None)
    order = request.args.get('order', None)

    return jsonify(service.get_all_short(size, page, filter, order)), 200


@ blue_print.route('<id>/files/<path>', methods=['GET'])
def get_file(id: str, path: str):

    file_name = path.split('/')[-1]
    file = service.get_file(id, path)

    return send_file(BytesIO(file),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=ntpath.basename(file_name))


@ blue_print.route('/status/<status>', methods=['DELETE'])
def delete_by_status(status: str):
    service.delete_by_status(Status(status))
    return '', 200
