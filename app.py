from flask import Flask,render_template, request, redirect, url_for, session,make_response,jsonify,flash
from werkzeug.security import generate_password_hash, check_password_hash
from model import *
from predict import CelebrityPredictionModel
from datetime import datetime,timedelta
app = Flask(__name__)

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10) 
predictor = CelebrityPredictionModel("./model")

# 회원가입 ID 체크
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
    if 'user_id' in session:
        if request.method=='POST':
            if Customer_DAO.duplicate_nickname(request.form['user_nickname']):
                result = {'duplicate' : 'True'}
                return make_response(jsonify(result),201)
            else:
                result = {'duplicate' : 'False'}
                return make_response(jsonify(result,201))
    else:
        return redirect('/main',200)

@app.route('/register',methods=['GET','POST'])
def register():
    if 'userid' not in session:
        print(request.form)
        if request.method == 'POST':
            id = request.form['userid']
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
                    # prinst
                    # return redirect('/',200)
                else:
                    return '실패'
        return render_template('register.html',msg='register loading succ')

@app.route('/login',methods=['GET','POST'])
def login():

    if 'user_id' in session:
        return redirect(url_for('main'))
    if request.method == 'POST':
        print(request.method)
        print(request.form['userid'])
    
        password = request.form['password']
        if Customer_DAO.check_login(request.form['userid'],password):
            print(request.form)
            session['user_id'] = request.form['userid']
            res = make_response(redirect('/'))
            res.set_cookie('userid',request.form['userid'])
            return redirect('/')
        else:
            flash("아이디와 비밀번호를 확인해 주세요")
            return redirect(url_for('login'))
    return render_template('loginM.html',msg='testing now')



@app.route('/',methods=['GET','POST'])
def main_view():
    # 
    input_time=datetime.now()
    if request.method=='POST':
        f = request.files['file']
        gender = int(request.form["gender_flag"])
        print(gender)
        print(f.filename.split('.')[-1])
        result = predictor
        if f.filename.split('.')[-1] in ['jpg','png','jpeg']:
            save_to = f'./static/img/' + input_time.strftime('%Y%m%d%H%M%S') +'.'+f.filename.split('.')[-1]
            # save_to = f'static/img/profiles/{user_id}'
            f.save(save_to)
            result = predictor.predict_img(gender,save_to)
            # 결과가 없는 경우 바로 alert창 나오는 영역
            if os.path.isfile(save_to):
                os.remove(save_to)
                print('file delete finish')
            # 사람이 아닐때
            if result == []:
                print("flash")
                flash('Not find humon')
                return render_template('main.html')
            # db에서 img 주소 추출
            img_src = simlityDAO.find_people(result[0][1])
            print(img_src)
            
            # 회원인경우 결과를 기반으로 DB에 정보저장해준다.
            if 'user_id' in session:
                if simlityDAO.check_result(userid=session['user_id']):
                    # simlityDAO.update_result
                    print(1)
                else:
                    print(2)
                    # simlityDAO.insert_result
            # 비회원의 경우

            return render_template('mainresult.html',imgsrc=img_src,results=result)
        # 파일 형식이 안맞을 경우
        else: 
            flash('지원가능한 파일형식은 jpg,png,jpeg입니다. 확인 후 재시도바랍니다.')
            return render_template('main.html')
    else:
        return render_template('main.html')
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
        return redirect('/main')
@app.route('/person',methods=['GET'])
def person():
    return render_template('pri.html')


#  get all은 쪽지함 조회 클릭시 기본적으로 보여주는 곳
@app.route('/note/all',methods=['GET','POST'])
def notes():
    if 'user_id'in session:
        return render_template('receivenote.html')
    else:     
        return redirect('/main',406)
@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect('/')
# @app.route('/notice/share',methods=['GET','POST'])
# def share_notice():
#     pass

# @app.route('/notice/free',method=['GET','POST'])
# def free_notice():
#     pass

# @app.route('/mypage/',methods=['GET','POST','DELETE','UPDATE'])
# def my_page():
#     pass
import os 


if __name__== '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug = True, port=8080,ssl_context='adhoc')