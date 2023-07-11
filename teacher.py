from flask import Flask,Blueprint, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta


teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')



@teacher_bp.route('/teacher_top', methods=['GET'])
def teacher_top():
    if 'user' in session:
        return render_template('teacher_top.html') # session があれば mypage.html を表示
    else:
        return redirect(url_for('index')) # session がなければログイン画面にリダイレクト

@teacher_bp.route('/student_register')
def student_register():
    return render_template('teacher_student_register.html')

@teacher_bp.route('/student_register_exe', methods=['POST'])
def student_register_exe():
    name=request.form.get('name')
    mail=request.form.get('mail')
    grade=request.form.get('grade')
    clas = request.form.get('class')
    year = request.form.get('year')
    year_1 = str(year)
    year2 = request.form.get('year2')
    year2_2 = str(year2)
    department=request.form.get('department')
    department2 = str(department)
    department3 = "未登録"
    class_num = request.form.get('class_num')
    class_num2 = int(class_num)
    student_num = year_1 + year2_2 + department2 
    
    for x in range(1, class_num2+1):
        if x < 10:
            x2 = str(x)
            student_num2 = student_num + "0" + x2
            password = student_num2
            db.insert_student(student_num2,name, mail,grade,clas,department3,password)
        else:
            x2 = str(x)
            student_num2 = student_num + x2
            password = student_num2
            db.insert_student(student_num2,name, mail,grade,clas,department3,password)
            
    msg='登録が完了しました。'
    return redirect(url_for('teacher.teacher_top', msg=msg))

@teacher_bp.route('/teacher_report_search')
def teacher_report_search():
    return render_template('teacher_report_search.html')

@teacher_bp.route('/teacher_report_search_exe', methods=['POST'])
def teacher_report_search_exe():
    company=request.form.get('company')
    industry=request.form.get('industry')
    result_type=request.form.get('result_type')
    grade=request.form.get('grade')
    clas=request.form.get('class')
    
    report_list=db.teacher_select_report(company, industry, result_type, grade, clas)
    
    return render_template('teacher_report_list.html', reports=report_list)

@teacher_bp.route('/teacher_report_detail', methods=['POST'])
def teacher_report_detail():
    company=request.form.get('company')
    student_num=request.form.get('student_num')
    
    report_detail=db.teacher_report_detail(company, student_num)
    
    return render_template('teacher_report_detail.html', detail=report_detail)

@teacher_bp.route('/teacher_approval', methods=['post'])
def teacher_approval():
    student_num = request.form.get('student_num')
    company=request.form.get('company')
    teacher_approval = request.form.get('teacher_approval')
    
    db.teacher_approval(company, student_num, teacher_approval)
    
    return redirect(url_for('teacher.teacher_top'))

@teacher_bp.route('/student_search')
def student_search():
    return render_template('teacher_student_search.html')

@teacher_bp.route('/student_search_exe', methods=['POST'])
def student_search_exe():
    name=request.form.get('name')
    department=request.form.get('department')
    grade=request.form.get('grade')
    clas=request.form.get('class')
    
    student_list=db.teacher_select_student(name, department, grade, clas)
    
    return render_template('teacher_student_list.html', students=student_list)

@teacher_bp.route('/teacher.student_del', methods=['POST'])
def student_del():
    checks=request.form.getlist('check')

    for sa in checks:
        db.teacher_delete_student(sa)
    
    return render_template('teacher_top.html')