from flask import Flask,render_template, request, redirect, url_for, session,make_response,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from model import Customer_DAO


app = Flask(__name__)
@app.route('/ckregister', method=['POST'])
def check_register():
    if request.mothed=='POST':
        if Customer_DAO.duplicate_member(request.form['userid']):
            result = {'duplicate : True'}
            return make_response(jsonify(result),201)
        else:
            reuslt = {'duplicate : False'}
            return make_response(jsonify(result,201))

@app.route('/register',methods=['GET','POST'])
def register():
    print(request.form)
    if request.method == 'POST':
        if Customer_DAO.duplicate_member(request.form['userid']):
            password =  generate_password_hash(request.form['password'])
            if Customer_DAO.register_member(request.form['userid'],password,request.form['user_nicname'],request.form['user_fullname'],request.form['birthday'],request.form['paper_flag'],request.form['gender_flag'],request.form['create_at']) :
                return '성공'
                # return redirect('/',200)
            else:
                return '실패'
    return render_template('register.html',msg='register loading succ')

@app.route('/login',methods=['GET','POST'])
def login():
    print(request.form)
    if request.method == 'POST':
        password = request.form['password']
        if Customer_DAO.check_login(request.form['username'],password):
            print(request.form)
            return '로그인 성공'
        else:
            return '로그인 실패'
    return render_template('login.html',msg='testing now')

# @app.route('/notice/share',methods=['GET','POST'])
# def share_notice():
#     pass

# @app.route('/notice/free',method=['GET','POST'])
# def free_notice():
#     pass

# @app.route('/mypage/',methods=['GET','POST'])
# def my_page():
#     pass



if __name__== '__main__':
    app.run(debug = True, port=8080)