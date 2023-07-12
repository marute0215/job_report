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
    
    count=db.insert_teacher(name, mail,password)
    
    if count==1:
        msg='登録が完了しました。'
        return redirect(url_for('admin_top', msg=msg))# Redirect でindex()にGet アクセス
    else:
        error='登録に失敗しました。'
        return render_template('admin_teacher_register.html', error=error)