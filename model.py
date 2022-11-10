import pymysql
import os
from flask import request, sessions
from werkzeug.security import generate_password_hash, check_password_hash

class Customer_DAO:
    def __init__(self): 
        pass

    def register_member(user_id,password,user_nickname,user_fullname,birthday,paper_flag,gender_flag,create_at):
        # 클라우드로 배포시 사용 예정
        # db = pymysql.connect(host=os.getenv('db_host'),user=os.getenv('db_user'),password=os.getenv('db_password'),db='test_db')
        
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
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


class Note_Dao:
    def __init__(self): 
        pass
    def send_note(sender_id,receiver_id, title, content,create_at):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        curs = db.cursor()
        
        sql = f'''insert customers values(null,"{sender_id}", "{receiver_id}", "{title}", "{content}", "{create_at}");'''
        print(sql)
        try:
            curs.execute(sql)
        except:
            db.close()
            return False
        db.commit()
        db.close()
        return True
    # 보낸 쪽지함 조회
    def view_send(sender_id):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        curs = db.cursor()
        
        sql =f'''select receiver_id, title, create_at from note_table where sender_id = "{sender_id}" order by create_at desc;'''
        try:
            curs.execute(sql)
            result = curs.fetchall()
        except:
            db.close()
            return []
        db.close()    
        return result

    # 수신 쪽지 내용 조회
    def detail_view(sender_id,receiver_id,title,create_at):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        curs = db.cursor()
        
        sql =f'''select sender_id,receiver_id, title, content, create_at from note_table where sender_id = "{sender_id}" and  receiver_id = "{receiver_id}" and create_at= "{create_at}";'''
        try:
            curs.execute(sql)
            result = curs.fetchall()
        except:
            db.close()
            return []
        db.close()    
        return result
    # 받은 쪽지함 조회
    def view_receive(sender_id):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        curs = db.cursor()
        
        sql =f'''select receiver_id, title, create_at, delete_at from note_table where sender_id = "{sender_id}" order by create_at desc;'''
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
    def delete_note(sender_id, receiver_id, title, content):
        db = pymysql.connect(host='localhost',user='root',password='1q2w3e4r',db='main')
        curs = db.cursor()
        
        sql =f'''select receiver_id, title, create_at from note_table where sender_id = "{sender_id}" order by create_at desc;'''
        try:
            curs.execute(sql)
            result = curs.fetchall()
        except:
            db.close()
            return []
        db.close()    
        return result