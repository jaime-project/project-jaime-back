from io import BytesIO

from flask import Blueprint, jsonify, request, send_file

from logic.apps.storage import service

blue_print = Blueprint('storage', __name__, url_prefix='/api/v1/storage')


@blue_print.route('/', methods=['POST'])
def upload_file():

    path_files = request.args.get('path', '/')

    for f in request.files.getlist('files'):
        service.upload_file(f.filename, path_files, f.stream)

    return '', 201


@blue_print.route('/<dir_name>', methods=['POST'])
def make_dir(dir_name: str):

    dir_path = request.args.get('path', '/')

    service.make_dir(dir_name, dir_path)

    return '', 201


@blue_print.route('/<file_name>', methods=['GET'])
def download_file(name: str):

    folder_path = request.args.get('path', '/')

    return send_file(BytesIO(service.download_file(name, folder_path)),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=name), 200


@blue_print.route('/', methods=['GET'])
def list_all():

    folder_path = request.args.get('path', '/')

    return jsonify(service.list_all(folder_path)), 200


@blue_print.route('/', methods=['GET'])
def get_detail():

    folder_path = request.args.get('path', '/')

    return jsonify(service.get_detail(folder_path).__dict__()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):

    folder_path = request.args.get('path', '/')

    service.delete(name, folder_path)

    return '', 200


@blue_print.route('/<name>', methods=['PUT'])
def put_dir_or_file(name):

    folder_path = request.args.get('path', '/')
    new_name = request.args.get('new_name')

    service.put_dir_or_file(name, folder_path, new_name)

    return '', 200
