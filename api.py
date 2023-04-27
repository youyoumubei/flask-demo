from flask import Blueprint

from flask import jsonify

def json_response(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        response = jsonify({"data": result})  # 创建一个JSON格式响应
        response.status_code = 200  # 设置响应状态码
        response.headers.add('Access-Control-Allow-Origin', '*')  # 添加CORS头部
        return response
    return wrapper

bp = Blueprint('api', __name__)

@bp.route('/users', methods=['GET'])
@json_response
def get_users_route():
    users = get_users()
    return {'users': users}

@bp.route('/users', methods=['POST'])
@json_response
def create_user_route():
    data = request.get_json()
    user = create_user(data)
    return {'user': user}

