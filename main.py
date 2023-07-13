from flask import Flask
from api import bp as api_bp
from api2 import bp as api2_bp
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')  # 使用Bearer令牌方案

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

# API路由函数
@app.route('/api/v1/myapi', methods=['GET'])
@auth.login_required  # 应用身份验证装饰器
@json_response  # 应用json_response装饰器
def my_api():
    id = int(request.args.get('id'))
    # 在这里执行您的API代码，使用传递的参数（id变量）
    result = {"message": f"Your API was called successfully with id={id}!"}
    return result

if __name__ == '__main__':
    app.run(port=8999)
