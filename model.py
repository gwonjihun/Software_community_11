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
        print(result)
        if check_password_hash(result[0][1],password):
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
