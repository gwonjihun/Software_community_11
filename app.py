from flask import Flask,render_template, request, redirect, url_for, session,make_response,jsonify,flash
from werkzeug.security import generate_password_hash, check_password_hash
from model import *
from predict import CelebrityPredictionModel
from datetime import datetime,timedelta
app = Flask(__name__)

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10) 
predictor = CelebrityPredictionModel(".\\model")

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
    input_time=datetime.now()
    input_time = input_time.strftime('%Y-%m-%d %H:%M:%S')
    if 'userid' not in session:
        print(request.form)
        if request.method == 'POST':
            id = request.form['userid']
            if id.isalnum() == False:
                flash('ID에 공백과 특수문자를 제외하고 입력하세요')
                return render_template('register.html')
            if Customer_DAO.duplicate_member(request.form['userid']):
                password =  generate_password_hash(request.form['password'])
                if Customer_DAO.register_member(request.form['userid'],password,request.form['user_nicname'],request.form['user_fullname'],request.form['birthday'],'1',request.form['gender_flag'],input_time) :
                    return redirect('/')
                    # prinst
                    # return redirect('/',200)
                else:
                    print(1)
                    flash('동일한 아이디, 닉네임이 존재합니다.')
                    return render_template('register.html')
        return render_template('register.html',msg='register loading succ')
    else:
        return redirect(url_for('main_view'))
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
            session['temp'] = Customer_DAO.get_temp(request.form['userid'])[0]

            return redirect(url_for('main_view'))
        else:
            flash("아이디와 비밀번호를 확인해 주세요")
            return redirect(url_for('login'))
    return render_template('loginM.html',msg='testing now')

@app.route('/myresult',methods=['GET','POST'])
def get_result():
    if 'user_id' in session:
        return render_template('mainresult.html')


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
            print(result)
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
                print(simlityDAO.check_result(userid=session['user_id']))
                Customer_DAO.add_temp(session['user_id'],1.5)
                session['temp'] = Customer_DAO.get_temp(session['user_id'])[0]
                print(session['user_id'])
                if simlityDAO.check_result(userid=session['user_id']):
                    # simlityDAO.update_result
                    simlityDAO.update_result(session['user_id'],result=result)
                else:
                    # 회원의 기존 사진이 없을 경우 insert 진행
                    simlityDAO.insert_result(session['user_id'],result)
                    # simlityDAO.insert_result
            # 비회원의 경우

            return render_template('mainresult.html',imgsrc=img_src,results=result)
        # 파일 형식이 안맞을 경우
        else: 
            flash('지원가능한 파일형식은 jpg,png,jpeg입니다. 확인 후 재시도바랍니다.')
            return render_template('main.html')
    else:
        return render_template('main.html')

@app.route('/simliarity',methods=['GET'])
def get_simliarity():
    if 'user_id' in session:
        user_id = session['user_id']
        result= simlityDAO.result_get(user_id)
        print(result)
        # '박보검', 73.59, '김수현', 19.0, '문빈', 2.92, '송강', 2.29, '정국', 1.12,
        return render_template('mainresult.html',results=result)
    else:
        return redirect(url_for('main_view'))

@app.route('/person',methods=['GET'])
def person():
    return render_template('pri.html')
@app.route('/list/free',methods=['GET','POST'])
def list_free():
    return render_template('listF.html')

@app.route('/list/share',methods=['GET','POST'])
def list_share():
    return render_template('listS.html')

@app.route('/update_info',methods=['GET','POST'])
def update_person():
    return render_template('Myinform.html')
#  get all은 쪽지함 조회 클릭시 기본적으로 보여주는 곳
@app.route('/note/send',methods=['GET','POST'])
def note_send():
    if 'user_id'in session:
        result = Note_Dao.view_send(session['user_id'])
        return render_template('sendnote.html',result=result)
    else:
        return '''
            <script>
            window.close()
            </script>
        '''

@app.route('/note/receive',methods=['GET','POST'])
def note_receive():
    if 'user_id'in session:

        temp= Note_Dao.view_receive(session['user_id'])
        
        return render_template('receivenote.html',result = temp)
    else:
        return '''
            <script>
            window.close()
            </script>
        '''

@app.route('/note/write',methods=['GET','POST'])
def note_write():
    current_at = datetime.now()
    current_at = current_at.strftime('%Y-%m-%d %H:%M:%S')
    if 'user_id' in session:
        if request.method =='POST':
            content = request.form['content']
            receive_id = request.form['receive_id']
            print(content,receive_id)
            Note_Dao.send_note(session['user_id'],receive_id,content,current_at)
            Customer_DAO.add_temp(session['user_id'],-5.0)
            session['temp'] = Customer_DAO.get_temp(session['user_id'])[0]
            print("session : ", session['temp'])
            return redirect(url_for('note_send'))
        else:
            receive_id = request.args.get('receive_id')
            return render_template('wirtenote.html',receive_id =receive_id)

    else:
        return '''
            <script>
            window.close()
            </script>
        '''
    
# kind=1이면 받은 메세지
# kind=0이면 보낸 메세지 삭제
@app.route('/note/delete',methods=['GET'])
def note_delete():
    if 'user_id' in session:
        id = request.args.get('id')
        content = request.args.get('content')
        create_at = request.args.get('create_at')
        # print(create_at)
        # create_at = datetime.strptime(create_at, '%Y-%m-%d %H:%M:%S')
        kind= request.args.get('kind')
        if kind == '1':
            Note_Dao.delete_note(id,session['user_id'],content,create_at)
            return redirect(url_for('note_receive'))
        else:
            Note_Dao.delete_note(session['user_id'],id,content,create_at)
            return redirect(url_for('note_send'))
    else:
        return redirect(url_for('main_view'))    


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
    # app.run(debug = True, port=8080,ssl_context='adhoc')
    app.run(debug = True, port=8080)