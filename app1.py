from flask import Flask, render_template, request, redirect, url_for, flash
import sys, os
from werkzeug.utils import secure_filename

sys.path.insert(0, ".")
from db.dbhelper import *

app = Flask(__name__)
app.secret_key = "supersecretkey123"


UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    students = getall('students')
    return render_template('index.html', studentlist=students)

@app.route("/add_student", methods=["POST"])
def add_student():
    idno = request.form.get('idno')
    lastname = request.form.get('lastname')
    firstname = request.form.get('firstname')
    course = request.form.get('course')
    level = request.form.get('level')

    if not idno or not lastname or not firstname or not course or not level:
        flash("All fields are required! Student not added.", "error")
        return redirect(url_for('index'))

    success = addrecord(
        'students',
        idno=idno,
        lastname=lastname,
        firstname=firstname,
        course=course,
        level=level
    )

    if success:
        flash(f"Student {firstname} {lastname} added successfully!", "success")
    else:
        flash("Error: Could not add student.", "error")

    return redirect(url_for('index'))

@app.route("/edit_student/<idno>")
def edit_student(idno):
    student = getrecord('students', idno=idno)
    if student:
        return render_template(
            'index.html',
            studentlist=getall('students'),  # MUST pass studentlist
            student_to_edit=student[0]
        )
    else:
        flash("Student not found", "error")
        return redirect(url_for('index'))

@app.route("/update_student/<idno>", methods=["POST"])
def update_student(idno):
    lastname = request.form.get('lastname')
    firstname = request.form.get('firstname')
    course = request.form.get('course')
    level = request.form.get('level')

    if not lastname or not firstname or not course or not level:
        flash("All fields are required! Student not updated.", "error")
        return redirect(url_for('edit_student', idno=idno))

    student = getrecord('students', idno=idno)
    filename = student[0]['image'] if student and student[0]['image'] else None

    image_file = request.files.get('image')
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    success = updaterecord(
        'students',
        idno=idno,
        lastname=lastname,
        firstname=firstname,
        course=course,
        level=level,
        image=filename
    )

    if success:
        flash(f"Student {firstname} {lastname} updated successfully!", "success")
    else:
        flash("Error: Could not update student.", "error")

    return redirect(url_for('index'))

@app.route("/delete_student/<idno>")
def delete_student(idno):
    student = getrecord('students', idno=idno)
    if student:
        deleterecord('students', idno=idno)
        flash(f"Student {student[0]['firstname']} {student[0]['lastname']} deleted successfully!", "success")
    else:
        flash("Student not found", "error")
    return redirect(url_for('index'))

# IMAGE UPLOAD ROUTE
@app.route("/upload_image/<idno>", methods=["POST"])
def upload_image(idno):
    if 'image' not in request.files:
        return {"success": False, "message": "No file part"}

    file = request.files['image']
    if file.filename == '':
        return {"success": False, "message": "No selected file"}

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Update student record with new image filename
        success = updaterecord('students', idno=idno, image=filename)
        if success:
            return {"success": True, "message": "Image uploaded successfully"}
        else:
            return {"success": False, "message": "Database update failed"}
    else:
        return {"success": False, "message": "Invalid file type"}

if __name__ == "__main__":
    app.run(debug=True)
