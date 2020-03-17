# coding:utf8
from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS


# 自定义模块
from db import db
import config

from app.dbsource.views import dbsource as dbsource_blueprint
from app.auth.views import auth as auth_blueprint
from app.home.views import home as home_blueprint
from app.admin.views import admin as admin_blueprint

from app.demo.views import demo as demo_blueprint


from middleware import Middleware

from flask_restful import Api, Resource

# 创建flask实例对象
app = Flask(__name__)
# 从config.py中导入配置信息
app.config.from_object(config.DevelopmentConfig)
app.config['JSON_SORT_KEYS'] = False

# 导入日志配置信息
config.DevelopmentConfig.init_app(app)

# 使用flask-sqlalchemy
db.init_app(app)

# 跨域设置
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# 设置JWT认证加密密钥
app.config['JWT_SECRET_KEY'] = '+\x1ba][o\x9e\x82\xa5MGsr\xa8x3\xc04\xd3\x0f\x11\x9a<z'
# 创建JWT实例对象
jwt = JWTManager(app)

# 注册中间件
# app.wsgi_app = Middleware(app.wsgi_app, request.path)

# 中间件
@app.before_request
def process_start_request():
    # print("正在访问： "+request.path)
    app.wsgi_app = Middleware(app.wsgi_app, request.path)
    # print(request.remote_addr)

@app.after_request
def process_end_request(response):
    print("结束访问： "+request.path)
    return response

# 注册自定义blueprint模块
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/api/admin")
app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
app.register_blueprint(dbsource_blueprint, url_prefix="/api/dbsource")


# 添加资源
from app.demo.views import TodoItem,HelloWorld,TodoSimple
from app.demo.views import api as demoapi
demoapi.add_resource(TodoItem, '/todos')
demoapi.add_resource(HelloWorld, '/hello')
demoapi.add_resource(TodoSimple, '/<string:todo_id>')

app.register_blueprint(demo_blueprint, url_prefix="/api/demo")



if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
