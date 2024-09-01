import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/mydb' 
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/mydb'  
     #如出現sql錯誤將':'後的數字改為xampp SQL的PORT number
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 's92080276@gmail.com'
    app.config['MAIL_PASSWORD'] = 'tqas gapa ywfg lpgq'

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user_management.login'  
 
    # 避免循環導入
    with app.app_context():
        from .models import User  

    # Blueprint
    from .user_management import user_management_bp
    from .account_binding import account_binding_bp
    from .signature_verification_api import signature_verification_bp
    from .evaluating_api import evaluation_bp
    #from .learningweb_api import stroke_order_bp
    app.register_blueprint(user_management_bp, url_prefix='/user_management')
    app.register_blueprint(account_binding_bp, url_prefix='/account_binding')
    app.register_blueprint(signature_verification_bp, url_prefix='/signature_verification')
    app.register_blueprint(evaluation_bp, url_prefix='/evaluation')
    #app.register_blueprint(stroke_order_bp ,url_prefix='/get_stroke_order')

    return app