from flask import Flask,Blueprint, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/admin_top', methods=['GET'])
def admin_top():
    if 'user' in session:
        return render_template('admin_top.html') # session があれば mypage.html を表示
    else:
        return redirect(url_for('index')) # session がなければログイン画面にリダイレクト

@admin_bp.route('/teacher_register')
def teacher_register():
    return render_template('admin_teacher_register.html')

@admin_bp.route('/teacher_register_exe', methods=['POST'])
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
    
    db.insert_teacher(name, mail,password)
    
    return render_template('admin_top.html')# Redirect でindex()にGet アクセス
    
@admin_bp.route('/report_search')
def report_search():
    return render_template('admin_report_search.html')

@admin_bp.route('/report_search_exe', methods=['POST'])
def report_search_exe():
    company=request.form.get('company')
    industry=request.form.get('industry')
    result_type=request.form.get('result_type')
    grade=request.form.get('grade')
    clas=request.form.get('class')
    
    report_list=db.admin_select_report(company, industry, result_type, grade, clas)
    
    return render_template('admin_report_list.html', reports=report_list)

@admin_bp.route('/report_detail', methods=['POST'])
def report_detail():
    company=request.form.get('company')
    student_num=request.form.get('student_num')
    
    report_detail=db.admin_report_detail(company, student_num)
    
    return render_template('admin_report_detail.html', detail=report_detail)

@admin_bp.route('/admin_approval', methods=['post'])
def admin_approval():
    student_num = request.form.get('student_num')
    company=request.form.get('company')
    approval = request.form.get('teacher_approval')
    
    db.admin_approval(company, student_num, approval)
    
    return redirect(url_for('admin.admin_top'))

@admin_bp.route('/student_search')
def student_search():
    return render_template('admin_student_search.html')

@admin_bp.route('/student_search_exe', methods=['POST'])
def student_search_exe():
    name=request.form.get('name')
    department=request.form.get('department')
    grade=request.form.get('grade')
    clas=request.form.get('class')
    
    student_list=db.teacher_select_student(name, department, grade, clas)
    
    return render_template('admin_student_list.html', students=student_list)

@admin_bp.route('/report_del', methods=['POST'])
def report_del():
    student_num = request.form.get('student_num')
    company=request.form.get('company')
    
    db.report_del(company, student_num)
    
    return redirect(url_for('admin.admin_top'))

@admin_bp.route('/teacher_list')
def teacher_list():

    teacher_list=db.teacher_list()
    
    return render_template('admin_teacher_list.html', teachers=teacher_list)

@admin_bp.route('/student_del', methods=['POST'])
def student_del():
    checks=request.form.getlist('check')

    for sa in checks:
        db.teacher_delete_student(sa)
    
    return render_template('admin_top.html')

@admin_bp.route('/teacher_del', methods=['POST'])
def teacher_del():
    checks=request.form.getlist('check')

    for sa in checks:
        db.admin_delete_teacher(sa)
    
    return render_template('admin_top.html')