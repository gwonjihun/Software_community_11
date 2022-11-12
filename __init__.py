from flask import Flask,render_template, request, redirect, url_for, session,make_response,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from model import Customer_DAO


app = Flask(__name__)

@app.route('/register/check/id', methods=['POST'])
def check_register_userid():
    if request.method=='POST':
        if Customer_DAO.duplicate_member(request.form['userid']):
            result = {'duplicate' : 'True'}
            return make_response(jsonify(result),201)
        else:
            result = {'duplicate' : 'False'}
            return make_response(jsonify(result,201))

@app.route('/register/check/nickname', methods=['POST'])
def check_register_nickname():
    if session['user_id']:
        if request.method=='POST':
            if Customer_DAO.duplicate_nickname(request.form['user_nickname']):
                result = {'duplicate' : 'True'}
                return make_response(jsonify(result),201)
            else:
                result = {'duplicate' : 'False'}
                return make_response(jsonify(result,201))
    else:
        return redirect('/',200)

# @app.route('/mypage/update', methods=['POST'])
#     # if session['user_id']:
#     #     if request.
#     # else:
#     #     return redirect('/')

# get -> 마이페이지 출력
# post ->user정보 수정
@app.route('/info',methods=['GET','POST'])
def mypage():
    if session['user_id']:
        if request.method =='POST':
            print()
        elif request.method =='GET':
            print()
            return render_template('mypage.html')
    else:
        #  세션이 존재 x이면 닮은꼴 입력하는 초기 화면으로 진행한다.
        return redirect('/')
@app.route('/register',methods=['GET','POST'])
def register():
    print(request.form)
    if request.method == 'POST':
        id = request.form['user_id']
        if id.isalnum() == False:
            result = {
                'space' : True,
                'msg ' : '공백 문자 존재'
            }
            return make_response(jsonify(result),401)
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
    if session['user_id']:
        return render_template('main.html')
    if request.method == 'POST':
        password = request.form['password']
        if Customer_DAO.check_login(request.form['username'],password):
            print(request.form)
            session['user_id'] = request.form['username']
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

# @app.route('/mypage/',methods=['GET','POST','DELETE','UPDATE'])
# def my_page():
#     pass

@app.route('/file_upload',methods = ['GET','POST'])
def file():
    return '''<form action="/file_upload" method="POST" enctype = "multipart/form-data">
            <input type = "file" name = "file" />            
            <input type='submit'>
            '''
@app.route('/file_upload',methods = ['GET','POST'])
def file():
    if request.method == 'POST':
        file = request.files['file']
        f = file.read()
        name = file.filename
        with open(name,'wb') as F:
            F.write(f)
        return redirect('/login')

    return '''<form action="/file_upload" method="POST" enctype = "multipart/form-data">
            <input type = "file" name = "file" />            
            <input type='submit'>
            '''
if __name__== '__main__':
    app.run(debug = True, port=8080)