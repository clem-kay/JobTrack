from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Database Model
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    specialization = db.Column(db.Text)
    tsc_attended = db.Column(db.Text)
    completion_year = db.Column(db.Integer)
    digital_address = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    telephone = db.Column(db.Text)
    city = db.Column(db.Text)
    region = db.Column(db.Text)
    country = db.Column(db.Text)
    current_job_title = db.Column(db.Text)
    current_employer = db.Column(db.Text)
    industry_or_sector = db.Column(db.Text)


# Routes
@app.route('/')
def index():
    # Check if the database file exists
    db_exists = os.path.exists('instance/student.db')

    # Check if the table exists in the database
    if not db_exists:
        db.create_all()
        print("Database and table created successfully!")

    # Proceed with fetching and rendering the students
    search_query = request.args.get('search', '')
    students = Student.query.filter(
        (Student.name.contains(search_query)) |
        (Student.email.contains(search_query)) |
        (Student.telephone.contains(search_query)) |
        (Student.student_id.contains(search_query))
    ).all()
    return render_template('index.html', students=students, search_query=search_query)


@app.route('/add', methods=['POST'])
def add_student():
    form_data = request.form
    new_student = Student(
        student_id=form_data['student_id'],
        name=form_data['name'],
        specialization=form_data.get('specialization', ''),
        tsc_attended=form_data.get('tsc_attended', ''),
        completion_year=form_data.get('completion_year', None),
        digital_address=form_data.get('digital_address', ''),
        email=form_data['email'],
        telephone=form_data.get('telephone', ''),
        city=form_data.get('city', ''),
        region=form_data.get('region', ''),
        country=form_data.get('country', ''),
        current_job_title=form_data.get('current_job_title', ''),
        current_employer=form_data.get('current_employer', ''),
        industry_or_sector=form_data.get('industry_or_sector', '')
    )
    db.session.add(new_student)
    db.session.commit()
    flash("Student added successfully!", "success")
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    form_data = request.form
    student.student_id = form_data['student_id']
    student.name = form_data['name']
    student.specialization = form_data.get('specialization', '')
    student.tsc_attended = form_data.get('tsc_attended', '')
    student.completion_year = form_data.get('completion_year', None)
    student.digital_address = form_data.get('digital_address', '')
    student.email = form_data['email']
    student.telephone = form_data.get('telephone', '')
    student.city = form_data.get('city', '')
    student.region = form_data.get('region', '')
    student.country = form_data.get('country', '')
    student.current_job_title = form_data.get('current_job_title', '')
    student.current_employer = form_data.get('current_employer', '')
    student.industry_or_sector = form_data.get('industry_or_sector', '')
    db.session.commit()
    flash("Student record updated successfully!", "success")
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student record deleted successfully!", "success")
    return redirect(url_for('index'))


@app.route('/import', methods=['POST'])
def import_excel():
    file = request.files['file']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        data = pd.read_excel(filepath,sheet_name='Tracking System',header=3)
        for _, row in data.iterrows():
            if not Student.query.filter_by(email=row['Email']).first():
                new_student = Student(
                    student_id=row['ID'],
                    name=row['Name'],
                    specialization=row.get('Specialization', ''),
                    tsc_attended=row.get('TSC Attended', ''),
                    completion_year=row.get('Completion Year', None),
                    digital_address=row.get('Digital Address', ''),
                    email=row['Email'],
                    telephone=row.get('Telephone', ''),
                    city=row.get('City', ''),
                    region=row.get('Region', ''),
                    country=row.get('Country', ''),
                    current_job_title=row.get('Current Job Title', ''),
                    current_employer=row.get('Current Employer', ''),
                    industry_or_sector=row.get('Industry or Sector', '')
                )
                db.session.add(new_student)
        db.session.commit()
        flash("Data imported successfully!", "success")
    else:
        flash("Please upload a file!", "danger")
    return redirect(url_for('index'))


@app.route('/export')
def export_excel():
    students = Student.query.all()
    data = pd.DataFrame([{
        'Student ID': s.student_id,
        'Name': s.name,
        'Specialization': s.specialization,
        'TSC Attended': s.tsc_attended,
        'Completion Year': s.completion_year,
        'Digital Address': s.digital_address,
        'Email': s.email,
        'Telephone': s.telephone,
        'City': s.city,
        'Region': s.region,
        'Country': s.country,
        'Current Job Title': s.current_job_title,
        'Current Employer': s.current_employer,
        'Industry or Sector': s.industry_or_sector
    } for s in students])
    filepath = os.path.join(UPLOAD_FOLDER, 'students_data.xlsx')
    data.to_excel(filepath, index=False)
    return send_file(filepath, as_attachment=True)


@app.route('/students', methods=['GET'])
def get_students():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)  # Page number
    per_page = 10  # Number of records per page

    # Filter students by search query if any
    students_query = Student.query.filter(Student.name.like(f'%{search_query}%'))

    # Paginate the students query
    students = students_query.paginate(page, per_page, False)

    students_data = [student.to_dict() for student in students.items]
    return jsonify({
        'students': students_data,
        'total_pages': students.pages,
        'current_page': students.page
    })


if __name__ == "__main__":
    app.run(debug=True)
