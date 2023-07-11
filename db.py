import os, psycopg2, string, random, hashlib
# DBへのコネクションを生成
def get_connection():
    url=os.environ['DATABASE_URL']
    connection=psycopg2.connect(url)
    return connection

def insert_admin(name, mail,password):
    sql='INSERT INTO AdminAccount VALUES (default, %s, %s,%s, %s)'
    salt=get_salt() # ソルトの生成
    hashed_password=get_hash(password, salt) # 生成したソルトでハッシュ
    try: # 例外処理
        connection=get_connection()
        cursor=connection.cursor()
        
        cursor.execute(sql, (name, mail, salt, hashed_password))
        count=cursor.rowcount# 更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError: # Java でいうcatch 失敗した時の処理をここに書く
        count=0# 例外が発生したら0 をreturn する。
        
    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()
    return count

def insert_teacher(name, mail,password):
    sql='INSERT INTO TeacherAccount VALUES (default, %s, %s,%s, %s)'
    salt=get_salt() # ソルトの生成
    hashed_password=get_hash(password, salt) # 生成したソルトでハッシュ
    try: # 例外処理
        connection=get_connection()
        cursor=connection.cursor()
        
        cursor.execute(sql, (mail, name, salt, hashed_password))
        count=cursor.rowcount# 更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError: # Java でいうcatch 失敗した時の処理をここに書く
        count=0# 例外が発生したら0 をreturn する。
        
    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()
    return count




def insert_student(student_num2,name, mail,grade,clas,department3,password):
    sql='INSERT INTO StudentAccount VALUES (default,%s, %s, %s, %s, %s, %s, %s, %s)'
    salt=get_salt() # ソルトの生成
    hashed_password=get_hash(password, salt) # 生成したソルトでハッシュ
   
    connection=get_connection()
    cursor=connection.cursor()
        
    cursor.execute(sql, (student_num2,name, mail, grade, clas, department3, salt, hashed_password))
    connection.commit()
        

    cursor.close()
    connection.close()

def teacher_select_report(company, industry, result_type, grade, clas):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT report.student_num, report.user_name, studentaccount.grade,\
                    studentaccount.class, report.company, report.industry, \
                    report.result_type, report.teachar_approval,\
                    TO_CHAR(report.register_date, 'YYYY/MM/DD HH24:MI') AS register_date\
            FROM report\
            INNER JOIN studentaccount ON report.student_num = studentaccount.student_num\
            WHERE report.company LIKE %s \
                AND report.industry LIKE %s \
                AND report.result_type LIKE %s \
                AND studentaccount.grade LIKE %s \
                AND studentaccount.class LIKE %s;"
    
    key='%'+company+'%'
    key2='%'+industry+'%'
    key3='%'+result_type+'%'
    key4='%'+grade+'%'
    key5='%'+clas+'%'
    cursor.execute(sql, (key, key2, key3, key4, key5))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def teacher_report_detail(company, student_num):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT student_num, user_name, company, industry, job,\
            firsttest_time, firsttest_type,\
            secondtest_time, secondtest_type,\
            thaadtest_time, thaadtest_type,\
            tesr_report, result_type, teachar_approval,\
            TO_CHAR(register_date, 'YYYY/MM/DD HH24:MI') AS register_date\
            FROM Report\
            where company = %s and student_num = %s"
    
    
    cursor.execute(sql, (company, student_num))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows


def teacher_approval(company, student_num, teacher_approval):
    sql='UPDATE report SET teachar_approval = %s where student_num = %s and company = %s'   
        
    connection=get_connection()
    cursor=connection.cursor()
    
    cursor.execute(sql, (teacher_approval,student_num, company))
    connection.commit()

    print(teacher_approval)
    
    cursor.close()
    connection.close()

def teacher_select_student(name, department, grade, clas):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT student_num, name, grade, class, department\
            FROM StudentAccount\
            WHERE name LIKE %s \
                AND department LIKE %s \
                AND grade LIKE %s \
                AND class LIKE %s;"
    
    key='%'+name+'%'
    key2='%'+department+'%'
    key3='%'+grade+'%'
    key4='%'+clas+'%'
    cursor.execute(sql, (key, key2, key3, key4,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def teacher_delete_student(sa):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM studentaccount WHERE student_num = %s;"
    
    cursor.execute(sql, (sa,))
    connection.commit()
    
    cursor.close()
    connection.close()
































def insert_report(student_num,name, company, industry, job, firsttest_time,firsttest_type,secondtest_time,secondtest_type,thaadtest_time,thaadtest_type,test_report, teacher_approval, admin_approval, resrul_type):
    sql='INSERT INTO report VALUES (default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,current_timestamp)'
    try: # 例外処理
        connection=get_connection()
        cursor=connection.cursor()
        
        cursor.execute(sql, (student_num,name, company, industry, job, firsttest_time,firsttest_type,secondtest_time,secondtest_type,thaadtest_time,thaadtest_type,test_report, teacher_approval, admin_approval, resrul_type))
        count=cursor.rowcount# 更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError: # Java でいうcatch 失敗した時の処理をここに書く
        count=0# 例外が発生したら0 をreturn する。
        
    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()
    return count

def select_report(company, industry, result_type):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT student_num, company, industry, job,\
            result_type, user_name,\
            TO_CHAR(register_date, 'YYYY/MM/DD HH24:MI') AS register_date\
            FROM Report \
            where company like %s and industry like %s and result_type like %s"
    
    key='%'+company+'%'
    key2='%'+industry+'%'
    key3='%'+result_type+'%'
    cursor.execute(sql, (key, key2, key3))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def select_report_detail(company, student_num):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT student_num, user_name, company, industry, job,\
            firsttest_time, firsttest_type,\
            secondtest_time, secondtest_type,\
            thaadtest_time, thaadtest_type,\
            tesr_report, result_type,\
            TO_CHAR(register_date, 'YYYY/MM/DD HH24:MI') AS register_date\
            FROM Report\
            where company = %s and student_num = %s"
    
    
    cursor.execute(sql, (company, student_num))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def select_account(student_num):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM StudentAccount where student_num = %s"
    
    cursor.execute(sql, (student_num, ))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def update_student_account(student_num,name,mail,grade,clas,department,password):
    sql='UPDATE StudentAccount SET name = %s, mail = %s, grade = %s, class = %s, department = %s, salt = %s, password = %s  WHERE student_num = %s'
    
    salt=get_salt() # ソルトの生成
    hashed_password=get_hash(password, salt) # 生成したソルトでハッシュ
   
    connection=get_connection()
    cursor=connection.cursor()
        
    cursor.execute(sql, (name,mail,grade,clas,department, salt, hashed_password,student_num))
    connection.commit()
        

    cursor.close()
    connection.close()

def select_report_student(student_num):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT student_num, company, industry, job,\
            result_type, user_name,\
            TO_CHAR(register_date, 'YYYY/MM/DD HH24:MI') AS register_date\
            FROM Report \
            where student_num = %s"
    
    cursor.execute(sql, (student_num,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def update_report(student_num,name, company, industry, job, firsttest_time,firsttest_type,secondtest_time,secondtest_type,thaadtest_time,thaadtest_type,test_report, resrul_type):
    sql='UPDATE report SET user_name = %s, industry = %s, \
            job = %s, firsttest_time = %s, firsttest_type = %s, secondtest_time = %s, secondtest_type = %s,\
            thaadtest_time = %s, thaadtest_type = %s, tesr_report = %s, result_type = %s WHERE student_num = %s and company = %s'
        
    connection=get_connection()
    cursor=connection.cursor()
        
    cursor.execute(sql, (name,industry, job, firsttest_time,firsttest_type,secondtest_time,secondtest_type,thaadtest_time,thaadtest_type,test_report, resrul_type, student_num, company))
    connection.commit()
        

    cursor.close()
    connection.close()



# ランダムなソルトを生成
def get_salt():
    # 文字列の候補(英大小文字+ 数字)
    charset = string.ascii_letters + string.digits
    # charset からランダムに30文字取り出して結合
    salt=''.join(random.choices(charset, k=30))
    return salt

# ソルトとPWからハッシュ値を生成
def get_hash(password, salt):
    b_pw=bytes(password, "utf-8")
    b_salt=bytes(salt, "utf-8")
    hashed_password=hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password

def login(user_name, password, user_type):
    
    if user_type == "student":
        sql = 'SELECT password, salt FROM StudentAccount WHERE student_num = %s'
    elif user_type == "teacher":
        sql = 'SELECT password, salt FROM TeacherAccount WHERE name = %s'
    elif user_type == "admin":
        sql = 'SELECT password, salt FROM AdminAccount WHERE name = %s'
    else:
        return False
    
    flg=False
    try :
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql, (user_name,))
        user=cursor.fetchone()
        if user!=None:
            # SQLの結果からソルトを取得
            salt=user[1]
            
            # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            hashed_password=get_hash(password, salt)
            
            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password==user[0]:
                flg=True
    except psycopg2.DatabaseError:
        flg=False
    finally:
        cursor.close()
        connection.close()
    return flg