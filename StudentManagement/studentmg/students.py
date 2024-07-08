from flask import (
    Blueprint, flash, g, redirect, render_template, request,jsonify
)

from studentmg.db import get_db,close_db

bp = Blueprint('studm',__name__)

@bp.route('/index',methods = ('GET','POST'))
def add_student():
    db = get_db()
    if request.method == 'POST':
        data = request.get_json()
        db.execute('INSERT INTO student (full_name,password,email) VALUES (?,?,?)',(data['full_name'],data['password'],data['email']))
        for subject in data['subjects']:
            db.execute('INSERT INTO student_subject (student_id, subjects, mark, grade) VALUES (?, ?, ?, ?)', 
                       (student_id, subject['subject'], subject['mark'], subject['grade']))
        db.commit()
        return 'Student added successfully'
    return 'Invalid'

@bp.route('/students/<int:student_id>', methods=('GET',))
def get_student(student_id):
    db = get_db()
    student = db.execute('SELECT * FROM student WHERE id = ?', (student_id,)).fetchone()
    if student is None:
        return 'student not found'
    student_data = {
        'id': student['id'],
        'full_name': student['full_name'],
        'password': student['password'],
        'email': student['email']
    }
    return jsonify(student_data)

@bp.route('/students/<int:student_id>', methods=('PUT'))
def update_student(student_id):
    db = get_db()
    student = db.execute('SELECT * FROM student WHERE id = ?', (student_id,)).fetchone()
    if student is None:
        return 'student not found'
    data = request.get_json()
    db.execute(
        'UPDATE student SET full_name = ?, password = ?, email = ? WHERE id = ?',
        (data['full_name'], data['password'], data['email'], student_id)
    )
    db.commit()
    return 'student updated successfully'

@bp.route('/students/<int:student_id>', methods=('DELETE'))
def delete_student(student_id):
    db = get_db()
    student = db.execute('SELECT * FROM student WHERE id = ?', (student_id,)).fetchone()
    if student is None:
        return 'Student not found'
    db.execute('DELETE FROM student WHERE id = ?', (student_id,))
    db.execute('DELETE FROM student_subject WHERE student_id = ?', (student_id,))
    db.commit()
    return  'Student deleted successfully'

