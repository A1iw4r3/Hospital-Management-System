from altair import Url
from flask import Flask, render_template, request, redirect, session, flash, url_for
import hashlib
import mysql.connector


app = Flask(__name__)
app.secret_key = 'your_secret_key'



# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="hys"
    )
    return conn

# Helper function to hash passwords
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/login/<user_type>', methods=['GET', 'POST'])
def login(user_type):
    if request.method == 'POST':
        print("POST request received")  # Debugging
        user_id = request.form['user_id']
        password = request.form['password']
        print(user_id, password)  # Debugging
        hashed_password = hash_password(password)
        if user_type == 'employee':
            query = "SELECT * FROM employee WHERE id = %s AND Password = %s"
            print("Employee login")  # Debugging
        elif user_type == 'patient':
            query = "SELECT * FROM patient WHERE id = %s AND Password = %s"
            print("Patient login")  # Debugging
        else:
            return "Invalid user type"
    
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (user_id, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user_id
            session['user_type'] = user_type
            if user_type == 'employee':
                print("Employee login successful")  # Debugging
                return redirect(url_for('employee_dashboard', user_type=user_type))
            else:
                print("Patient login successful")   # Debugging
                return redirect(url_for('patient_dashboard_details', patient_id=user_id))
        else:
            flash("Login failed!", "danger")
            return redirect(url_for('login', user_type=user_type))

    # Render the appropriate login form
    if user_type == 'employee':
        return render_template('employee_login.html', user_type=user_type)
    elif user_type == 'patient':
        return render_template('patient_login.html', user_type=user_type)
    else:
        flash("Invalid user type.", "danger")
        return redirect(url_for('home'))

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'user_id' in session and session['user_type'] == 'employee':
        print(session['user_id'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT designation FROM employee WHERE id = %s", (session['user_id'],))
        designation = cursor.fetchone()
        designation = designation[0]
        designation = designation.lower()
        print(designation)
        cursor.close()
        conn.close()
        if designation == 'administrator':
            return redirect('/administrator_dashboard')
        elif designation == 'nurse':
            return render_template('nurse_dashboard.html', designation=designation[0])
        else:
            return render_template(f'{designation}_dashboard.html', designation=designation[0])
    return redirect('/')


# Patient Details
@app.route('/patient_dashboard/<int:patient_id>')
def patient_dashboard_details(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get patient details
    cursor.execute("SELECT * FROM patient WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()

    # Get patient bills
    cursor.execute("SELECT * FROM bill WHERE Patient_ID = %s", (patient_id,))
    bill = cursor.fetchone()

    # Get patient's medicines
    cursor.execute("SELECT * FROM medicine WHERE Patient_ID = %s", (patient_id,))
    medicine = cursor.fetchall()

    # Get patient's reports
    cursor.execute("SELECT * FROM report WHERE Patient_ID = %s", (patient_id,))
    reports = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('patient_dashboard.html', patient=patient, bill=bill, medicine=medicine, reports=reports)

# Doctor Dashboard
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'user_id' not in session or session['user_type'] != 'employee':
        return redirect(url_for('login', user_type='employee'))
    
    patient_id = request.args.get('patient_id')
    print(f"Received patient_id: {patient_id}")
    conn = get_db_connection()
    cursor = conn.cursor()

    if patient_id:
        cursor.execute('SELECT * FROM patient WHERE id = %s', (patient_id,))
        patient = cursor.fetchone()
        print(f"Patient data: {patient}")
        cursor.execute('SELECT * FROM report WHERE Patient_ID = %s', (patient_id,))
        report = cursor.fetchone()
        cursor.execute('SELECT * FROM medicine WHERE Patient_ID = %s', (patient_id,))
        medicine = cursor.fetchone()
        print(f"Report data: {report}")
        print(f"Medicine data: {medicine}")
    else:
        patient = report = medicine = None
    
    cursor.close()
    conn.close()
    return render_template('doctor_dashboard.html', patient=patient, report=report, medicine=medicine)

# Edit/Add Medicine
@app.route('/edit_medicine', methods=['GET', 'POST'])
def edit_medicine():
    if 'user_id' not in session or session['user_type'] != 'employee':
        return redirect(url_for('login', user_type='employee'))

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        medicines = request.form['medicines']
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM medicine WHERE patient_id = %s', (patient_id,))
        existing_medicine = cursor.fetchone()
        
        if existing_medicine:
            cursor.execute('UPDATE medicine SET medicines = %s WHERE patient_id = %s', (medicines, patient_id))
        else:
            cursor.execute('INSERT INTO medicine (patient_id, medicines) VALUES (%s, %s)', (patient_id, medicines))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Medicine updated successfully.', 'success')
        return redirect(url_for('doctor_dashboard', patient_id=patient_id))
    
    return redirect(url_for('doctor_dashboard'))

# Edit/Add Report
@app.route('/edit_report', methods=['GET', 'POST'])
def edit_report():
    if 'user_id' not in session or session['user_type'] != 'employee':
        return redirect(url_for('login', user_type='employee'))

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        print(f"Received patient_id: {patient_id}")
        report = request.form['report']
        print(f"Received report: {report}")

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM report WHERE patient_id = %s', (patient_id,))
        existing_report = cursor.fetchone()
        
        if existing_report:
            cursor.execute('UPDATE report SET reports = %s WHERE patient_id = %s', (report, patient_id))
        else:
            cursor.execute('INSERT INTO report (patient_id, reports) VALUES (%s, %s)', (patient_id, report))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Report updated successfully.', 'success')
        return redirect(url_for('doctor_dashboard', patient_id=patient_id))
    
    return redirect(url_for('doctor_dashboard'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login', user_type='employee'))

# Admin Routes

# Display all employees and patients
@app.route('/administrator_dashboard')
def administrator_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()
    conn.close()

    return render_template('administrator_dashboard.html', employees=employees, patients=patients)

@app.route('/employee_adding')
def employee_adding():
    return render_template('add_employee.html')
@app.route('/patient_adding')
def patient_adding():
    return render_template('add_patient.html')

# Add employee
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        designation = request.form['designation']
        password = hash_password(request.form['password'])

        # max primary key value
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM employee")
        E_id = cursor.fetchone()[0]
        E_id+=1
        conn.close()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
    "INSERT INTO employee (id,Name, Gender, Email, Phone_number, Designation, Password) "
    "VALUES (%s,%s, %s, %s, %s, %s, %s)",
    (E_id,name, gender, email, phone, designation, password))
        
        conn.commit()
        conn.close()

        
        return redirect(url_for('administrator_dashboard'))
    return render_template('admin_dashboard.html', add_employee=True)

# Add patient
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        password = hash_password(request.form['password'])

        # max primary key value
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM patient")
        P_id = cursor.fetchone()[0]
        P_id+=1
        conn.close()

        

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patient (id,name, gender, email, phone_number, Password) VALUES (%s,%s, %s, %s, %s, %s)",
            (P_id,name, gender, email, phone, password)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('administrator_dashboard'))
    
    return render_template('admin_dashboard.html', add_patient=True)

@app.route('/edit_employee/<int:emp_id>', methods=['GET', 'POST'])
def edit_employee(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee WHERE ID = %s", (emp_id,))
    employee = cursor.fetchone()
    conn.close()

    if not employee:
        flash('Employee not found.', 'error')
        return redirect(url_for('view_employees'))

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        designation = request.form['designation']
        password = hash_password(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE employee
            SET name = %s, gender = %s, email = %s, phone_number = %s, designation = %s, password_hash = %s
            WHERE ID = %s""",
            (name, gender, email, phone, designation, password, emp_id)
        )
        conn.commit()
        conn.close()

        flash('Employee details updated successfully.', 'success')
        return redirect(url_for('view_employees'))

    return render_template('edit_employee.html', employee=employee)

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    # Retrieve the patient details based on patient_id
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE Patient_ID = %s", (patient_id,))
    patient = cursor.fetchone()
    conn.close()

    if not patient:
        flash('Patient not found.', 'error')
        return redirect(url_for('view_patients'))  # Redirect to patient list if not found

    # If the request is POST, update the patient details
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        password = hash_password(request.form['password'])

        # Update patient details in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE patients
            SET name = %s, gender = %s, email = %s, phone = %s, password_hash = %s
            WHERE Patient_ID = %s""",
            (name, gender, email, phone, password, patient_id)
        )
        conn.commit()
        conn.close()

        flash('Patient details updated successfully.', 'success')
        return redirect(url_for('view_patients'))  # Redirect to patient list after update
 
    # Render the edit patient form with the current patient data
    return render_template('edit_patient.html', patient=patient)
 
@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    # Connect to the database and delete the patient
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patient WHERE id = %s", (patient_id,))
    conn.commit()
    conn.close()

    flash('Patient deleted successfully.', 'success')
    return redirect(url_for('administrator_dashboard'))

@app.route('/delete_employee/<int:emp_id>', methods=['POST'])
def delete_employee(emp_id):
    # Connect to the database and delete the employee
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employee WHERE id = %s", (emp_id,))
    conn.commit()
    conn.close()

    flash('Employee deleted successfully.', 'success')
    return redirect(url_for('administrator_dashboard'))  # Redirect back to the employee list

@app.route('/nurse_dashboard')
def nurse_dashboard():
    if 'user_id' not in session or session['user_type'] != 'employee':
        return redirect(url_for('login', user_type='employee'))
    
    patient_id = request.args.get('patient_id')
    print(f"Received patient_id: {patient_id}")
    conn = get_db_connection()
    cursor = conn.cursor()

    if patient_id:
        cursor.execute('SELECT * FROM patient WHERE id = %s', (patient_id,))
        patient = cursor.fetchone()
        print(f"Patient data: {patient}")
        cursor.execute('SELECT * FROM report WHERE Patient_ID = %s', (patient_id,))
        report = cursor.fetchone()
        cursor.execute('SELECT * FROM medicine WHERE Patient_ID = %s', (patient_id,))
        medicine = cursor.fetchone()
        print(f"Report data: {report}")
        print(f"Medicine data: {medicine}")
    else:
        patient = report = medicine = None
    
    cursor.close()
    conn.close()
    return render_template('nurse_dashboard.html', patient=patient, report=report, medicine=medicine)

# Edit/Delete Employee and Patient functions are unchanged and similar to the ones above

if __name__ == '__main__':
    app.run(debug=True)
