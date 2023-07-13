from flask import Flask
from api import bp as api_bp
from api2 import bp as api2_bp
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')  # 使用Bearer令牌方案

# 配置日志
log_file = 'api.log'
handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=30)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# 可选：将日志输出到文件
# logging.basicConfig(filename='api.log', level=logging.INFO)


app.register_blueprint(api_bp, url_prefix='/api/v1')
app.register_blueprint(api2_bp, url_prefix='/api/v2')


# 假设您有一个字典，其中包含了用户ID和对应的令牌
users = {
    "user1": "token1",
    "user2": "token2",
    "user3": "token3"
}

# 身份验证回调函数
@auth.verify_token
def verify_token(token):
    if token in users.values():
        return True
    else:
        return False

def authenticate(func):
    def wrapper(*args, **kwargs):
        # 在这里进行权限校验逻辑
        if not check_auth():
            return jsonify({"error": "Unauthorized"}), 401  # 返回 401 错误的 JSON 响应
        return func(*args, **kwargs)
    return wrapper

def json_response(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        response = jsonify({"data": result})  # 创建一个JSON格式响应
        response.status_code = 200  # 设置响应状态码
        response.headers.add('Access-Control-Allow-Origin', '*')  # 添加CORS头部
        return response
    return wrapper

# 配置日志
logging.basicConfig(level=logging.INFO)  # 设置日志级别为 INFO
logger = logging.getLogger('api')  # 创建一个名为 'api' 的日志记录器

# 请求钩子函数 - 在请求开始时记录请求信息
@app.before_request
def log_request_info():
    logger.info('Request: %s %s', request.method, request.path)
    logger.info('Request headers: %s', request.headers)
    logger.info('Request body: %s', request.get_json())

# 请求钩子函数 - 在请求结束时记录响应信息
@app.after_request
def log_response_info(response):
    logger.info('Response status: %s', response.status)
    logger.info('Response headers: %s', response.headers)
    logger.info('Response body: %s', response.get_data())
    return response

# API路由函数
@app.route('/api/v1/myapi', methods=['GET'])
@auth.login_required  # 应用身份验证装饰器
@json_response  # 应用json_response装饰器
def my_api():
    app.logger.info('This is an information log.') 
    id = int(request.args.get('id'))
    # 在这里执行您的API代码，使用传递的参数（id变量）
    result = {"message": f"Your API was called successfully with id={id}!"}
    return result

if __name__ == '__main__':
    app.run(port=8999)
