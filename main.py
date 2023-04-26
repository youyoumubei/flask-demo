from flask import Flask
from api import api_routes  # 导入包含API路由的文件

app = Flask(__name__)
app.register_blueprint(api_routes)  # 添加API路由到应用程序对象

if __name__ == '__main__':
    app.run(port=8999)
