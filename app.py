from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta
from teacher import teacher_bp

app=Flask(__name__)
app.register_blueprint(teacher_bp)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))


@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')# Redirect された時のパラメータ受け取り
    
    if msg==None:
        # 通常のアクセスの場合
        return render_template('index.html')
    else:
        # register_exe() からredirect された場合
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    user_name=request.form.get('username')
    session['user_name'] = user_name
    password=request.form.get('password')
    user_type=request.form.get('usertype')
    
    # ログイン判定
    if db.login(user_name, password, user_type):
        
        if user_type == "admin":
            session['user'] =True# session にキー：'user', バリュー:True を追加
            session.permanent=True# session の有効期限を有効化
            app.permanent_session_lifetime = timedelta(minutes=30) # session の有効期限を 5 分に設定
            return redirect(url_for('admin_top'))
        elif user_type == "teacher":
            session['user'] =True# session にキー：'user', バリュー:True を追加
            session.permanent=True# session の有効期限を有効化
            app.permanent_session_lifetime = timedelta(minutes=30) # session の有効期限を 5 分に設定
            return redirect(url_for('teacher.teacher_top'))
        elif user_type == "student":
            session['user'] =True# session にキー：'user', バリュー:True を追加
            session.permanent=True# session の有効期限を有効化
            app.permanent_session_lifetime = timedelta(minutes=30) # session の有効期限を 5 分に設定
            return redirect(url_for('mypage'))
        
    else:
        error='ユーザ名またはパスワードが違います。'
        
        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data={'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)
    
@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html') # session があれば mypage.html を表示
    else:
        return redirect(url_for('index')) # session がなければログイン画面にリダイレクト
    
@app.route('/report_register')
def report_register():
    return render_template('report_register.html')

@app.route('/report_register_exe', methods=['POST'])
def report_register_exe():
    student_num=request.form.get('student_num')
    name=request.form.get('name')
    company=request.form.get('company')
    industry=request.form.get('industry')
    job=request.form.get('job')
    firsttest_time=request.form.get('firsttest_time')
    firsttest_type=request.form.get('firsttest_type')
    secondtest_time=request.form.get('secondtest_time')
    secondtest_type=request.form.get('secondtest_type')
    thaadtest_time=request.form.get('thaadtest_time')
    thaadtest_type=request.form.get('thaadtest_type')
    test_report = request.form.get('test_report')
    teacher_approval=request.form.get('teacher_approval')
    admin_approval=request.form.get('admin_approval')
    resrul_type = request.form.get('result_type')
    
    
    count=db.insert_report(student_num,name, company, industry, job, firsttest_time,firsttest_type,secondtest_time,secondtest_type,thaadtest_time,thaadtest_type,test_report, teacher_approval, admin_approval, resrul_type)
    
    if count==1:
        msg='登録が完了しました。'
        return redirect(url_for('mypage', msg=msg))# Redirect でindex()にGet アクセス
    else:
        error='登録に失敗しました。'
        return render_template('report_register.html', error=error) 

@app.route('/report_search')
def report_search():
    return render_template('report_search.html')

@app.route('/report_search_exe', methods=['POST'])
def report_search_exe():
    company=request.form.get('company')
    industry=request.form.get('industry')
    result_type=request.form.get('result_type')
    
    report_list=db.select_report(company, industry, result_type)
    
    return render_template('report_list.html', reports=report_list)

@app.route('/report_detail', methods=['POST'])
def report_detail():
    company=request.form.get('company')
    student_num=request.form.get('student_num')
    
    report_detail=db.select_report_detail(company, student_num)
    
    return render_template('report_detail.html', detail=report_detail)

@app.route('/account_search', methods=['GET'])
def account_search():
    student_num = session['user_name']
    
    student_list=db.select_account(student_num)
    
    return render_template('student_account.html', account=student_list)

@app.route('/account_update', methods=['GET'])
def account_update():
    
    return render_template('student_account_update.html')

@app.route('/student_update_exe', methods=['POST'])
def student_update_exe():
    student_num = session['user_name']
    name=request.form.get('name')
    mail=request.form.get('mail')
    grade=request.form.get('grade')
    clas=request.form.get('class')
    department=request.form.get('department')
    password=request.form.get('password')

    db.update_student_account(student_num,name,mail,grade,clas,department,password)
    return redirect(url_for('mypage'))# Redirect でindex()にGet アクセス 

@app.route('/report_update_list', methods=['GET'])
def report_update_list():
    student_num = session['user_name']
    
    report_list=db.select_report_student(student_num)
    
    return render_template('student_report_list.html', reports=report_list)

@app.route('/report_update', methods=['post'])
def report_update():
    student_num = request.form.get('student_num')
    company=request.form.get('company')
    
    report_detail=db.select_report_detail(company, student_num)
    
    return render_template('report_update_form.html',detail=report_detail)

@app.route('/report_update_exe', methods=['POST'])
def report_update_exe():
    student_num=request.form.get('student_num')
    name=request.form.get('name')
    company=request.form.get('company')
    industry=request.form.get('industry')
    job=request.form.get('job')
    firsttest_time=request.form.get('firsttest_time')
    firsttest_type=request.form.get('firsttest_type')
    secondtest_time=request.form.get('secondtest_time')
    secondtest_type=request.form.get('secondtest_type')
    thaadtest_time=request.form.get('thaadtest_time')
    thaadtest_type=request.form.get('thaadtest_type')
    test_report = request.form.get('test_report')
    resrul_type = request.form.get('result_type')
    
    
    db.update_report(student_num,name, company, industry, job, firsttest_time,firsttest_type,secondtest_time,secondtest_type,thaadtest_time,thaadtest_type,test_report, resrul_type)
    
    return redirect(url_for('mypage'))# Redirect でindex()にGet アクセス

















@app.route('/admin_top', methods=['GET'])
def admin_top():
    if 'user' in session:
        return render_template('admin_top.html') # session があれば mypage.html を表示
    else:
        return redirect(url_for('index')) # session がなければログイン画面にリダイレクト

@app.route('/teacher_register')
def teacher_register():
    return render_template('admin_teacher_register.html')

@app.route('/teacher_register_exe', methods=['POST'])
def teacher_register_exe():
    name=request.form.get('name')
    mail=request.form.get('mail')
    password=request.form.get('password')
    
    # バリデーションチェック
    if name=='':
        error='ユーザ名が未入力です'
        return render_template('admin_teacher_register.html', error=error)
    
    if password=='':
        error='パスワードが未入力です'
        return render_template('admin_teacher_register.html', error=error)
    
    count=db.insert_teacher(name, mail,password)
    
    if count==1:
        msg='登録が完了しました。'
        return redirect(url_for('admin_top', msg=msg))# Redirect でindex()にGet アクセス
    else:
        error='登録に失敗しました。'
        return render_template('admin_teacher_register.html', error=error)



@app.route('/logout')
def logout():
    session.pop('user', None) # session の破棄
    return redirect(url_for('index')) # ログイン画面にリダイレクト

if __name__ == '__main__':
	app.run(debug=True)