import pymysql
import os
from flask import request, sessions
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
class Customer_DAO:
    def __init__(self): 
        pass

    def add_temp(user_id,temp:float):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        # 활동온도는 초기 36.5도로 고정
        sql = f'''update customers set activite_temp = activite_temp + {temp} where user_id = '{user_id}';'''
        print(sql)
        try:
            curs.execute(sql)
            print("@@@@@@@@@@@@@@@@@@@@@@2")
            print("update succ")
        except:
            print("cutomser update error!")
            return []
        db.commit()
        db.close()
        
    def get_temp(user_id):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        # 활동온도는 초기 36.5도로 고정
        sql = f'''select activite_temp from customers where user_id = "{user_id}";'''
        print(sql)
        try:
            curs.execute(sql)
            result = curs.fetchone()
        except:
            print("cutomser insert error!")
            return []
        db.commit()
        db.close()
        return result

    def register_member(user_id,password,user_nickname,user_fullname,birthday,paper_flag,gender_flag,create_at):
        # 클라우드로 배포시 사용 예정
        # db = pymysql.connect(host=os.getenv('db_host'),user=os.getenv('db_user'),password=os.getenv('db_password'),db='test_db')
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        # 활동온도는 초기 36.5도로 고정
        sql = f'''insert customers values(null,"{user_id}","{password}","{user_nickname}","{user_fullname}","{birthday}",{paper_flag},{gender_flag},36.5,0,"{create_at}",null,"{create_at}",null);'''
        print(sql)
        try:
            curs.execute(sql)
        except:
            print("cutomser insert error!")
            return 
        db.commit()
        db.close()
        return True

    def check_login(user_id,password):
        print(password)
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        # 활 동온도는 초기 36.5도로 고정
        sql = f'''select user_id, password from customers where user_id = "{user_id}"''' 
        curs.execute(sql)
        result = curs.fetchall()
        cnt = curs.rowcount
        print(result)
        if cnt and check_password_hash(result[0][1],password):
            print('로그인 성공')
            return True
        else:
            return False

    def duplicate_member(user_id):
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        curs = db.cursor()
        
        sql = f'''select * from customers where user_id ="{user_id}"'''
        print(sql)
        curs.execute(sql)
        
        result = curs.rowcount
        
        if result == 0 :
            db.commit()
            db.close()
            return True
        else:
            db.commit()
            db.close()
            return False

    def duplicate_nickname(user_nickname):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        
        sql = f'''select * from customers where user_nickname ="{user_nickname}"'''
        print(sql)
        curs.execute(sql)
        
        result = curs.rowcount
        
        if result == 0 :
            db.commit()
            db.close()
            return True
        else:
            db.commit()
            db.close()
            return False
# class Noticce_Dao:
#     def __init__(self):
#         pass

#     def write_note():
#         pass

#     def get_note_

class Note_Dao:
    def __init__(self): 
        pass
    def send_note(sender_id,receiver_id, content,create_at):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        
        sql = f'''insert into note_table values(null,"{sender_id}", "{receiver_id}", "{content}", "{create_at}",null);'''
        print(sql)
        try:
            curs.execute(sql)
        except:
            db.close()
            print('note insert failed')
            return False
        db.commit()
        db.close()
        print('note insert suc')
        return True

    # 보낸 쪽지 조회
    def view_send(sender_id):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        
        sql =f'''select receiver_id, content, create_at from note_table where sender_id = "{sender_id}" order by create_at desc;'''
        try:
            curs.execute(sql)
            result = curs.fetchall()
            print(result)
        except:
            db.close()
            return []
        db.close()    
        return result
    # 받은 쪽지함 조회
    def view_receive(sender_id):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        
        sql =f'''select sender_id, content, create_at from note_table where receiver_id = "{sender_id}" order by create_at desc;'''
        try:
            curs.execute(sql)
            result = curs.fetchall()
        except:
            db.close()
            return []
        db.close()    
        return result

    # 보낸 쪽지 삭제 보낸 쪽지 리스트는 지울 수 없음
    # but, 수신자는 해당 쪽지를 지울 수 있음
    def delete_note(sender_id, receiver_id, content, create_at):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        
        sql =f'''delete from note_table where sender_id = "{sender_id}" and receiver_id = "{receiver_id}" and content = "{content}" and create_at="{create_at}";'''
        print(sql)
        try:
            curs.execute(sql)
        except Exception as e:
            print(e)
            db.close()
        print('delete finish')
        db.commit()
        db.close()    
    
from datetime import datetime

class simlityDAO:
    def __init__(self): 
        pass
    
    def result_get(userid):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        sql = f'''select * from similarity_table where user_id = "{userid}"'''
        try:
            curs.execute(sql)
            result = curs.fetchone()
        except Exception as e :
            print(e)
            db.close()
            print('similarity table data searach failed')
            return []
        print("ERQWERQWERQWERQWERQWERQWERQWER")
        print(result)
        db.commit()
        db.close()
        return result

    def check_result(userid):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        sql = f'''select user_id from similarity_table where user_id = "{userid}"'''
        try:
            curs.execute(sql)
            result = curs.rowcount
        except Exception as e :
            print(e)
            db.close()
            return False
        print("ERQWERQWERQWERQWERQWERQWERQWER")
        print(result)
        if result <=0:
            return False
        db.commit()
        db.close()
        return True

    
    def update_result(userid,result):
        # result 형식
        # ('95.123' '고창성)
        cur_time = datetime.now()
        cur_time = cur_time.strftime('%Y-%m-%d %H:%M:%S')
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        sql = f'''update similarity_table set result_1st = "{result[0][1]}", percent_1st = {round(result[0][0],2)}, result_2nd = "{result[1][1]}" ,percent_2nd = {round(result[1][0],2)} ,result_3rd = "{result[2][1]}", percent_3rd = {round(result[2][0],2)}, result_4th = "{result[3][1]}", percent_4th = {round(result[3][0],2)}, result_5th = "{result[4][1]}", percent_5th = {round(result[4][0],2)}, create_at = "{cur_time}", update_at = "{cur_time}"'''
        try:
            curs.execute(sql)
            print("update succ")
        except:
            db.close()
            print("update failed")
        db.commit()
        db.close()

    def insert_result(userid,result):
        cur_time = datetime.now()
        cur_time = cur_time.strftime('%Y-%m-%d %H:%M:%S')
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        print(f'''null,"userid", "{result[0][1]}","{round(result[0][0],2)}",  "{result[0][1]}" , {round(result[1][0],2)} , "{result[1][1]}" ,  {round(result[2][0],2)} ,"{result[2][1]}" ,{round(result[3][0],2)} , "{result[4][1]}" , {round(result[4][0],2)} , "{cur_time}" ,null,"{cur_time}"''')
        sql = f'''insert into similarity_table value(null,"{userid}", "{result[0][1]}",{round(result[0][0],2)},  "{result[0][1]}" , {round(result[1][0],2)} , "{result[1][1]}" ,  {round(result[2][0],2)} ,"{result[2][1]}" ,{round(result[3][0],2)} , "{result[4][1]}" , {round(result[4][0],2)} , "{cur_time}" ,null,"{cur_time}");'''
        print(sql)
        try:
            curs.execute(sql)
            print("insert succ")
        except:
            db.close()
            print("insert failed")
            return
        db.commit()
        db.close()
    def find_people(picname):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        tdb = pymysql.connect(host='software-webservice-11.mysql.database.azure.com',user='roots',password='rnjswlgns1!',db='main',ssl_ca='./static/cert/DigiCertGlobalRootCA.crt.pem')
        curs = db.cursor()
        result=[]
        sql = f'''select pic_add from image_info where pic_name = '{picname}';'''
        print(sql)
        try:
            curs.execute(sql)
            result = curs.fetchone()

        except:
            db.close()
            return []
        db.commit()
        db.close()
        return result
