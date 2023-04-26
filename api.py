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


api_routes = Blueprint('api', __name__)

@api_routes.route('/api/v1/hello', methods=['GET'])
def hello():
    return 'Hello, World!'
 
from flask import Flask
from api import api_routes
from my_decorators import json_response  # 导入自定义的装饰器函数

app = Flask(__name__)
app.register_blueprint(api_routes)

@app.route('/api/v1/myapi', methods=['POST'])
@json_response  # 应用json_response装饰器
def my_api():
    data = request.get_json()
    # 在这里执行您的API代码，使用传递的参数（data变量）
    result = {"message": "Your API was called successfully!"}
    return result  # 返回结果，将由装饰器转换为JSON格式响应
