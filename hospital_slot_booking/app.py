from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock data for hospital comparison and slot bookings
hospitals = [
    {'name': 'Hospital A', 'rating': 4.5, 'facilities': 'ICU, Surgery, Emergency'},
    {'name': 'Hospital B', 'rating': 4.7, 'facilities': 'ICU, Surgery, Blood Bank'},
    {'name': 'Hospital C', 'rating': 4.2, 'facilities': 'ICU, Emergency'}
]

booked_slots = []  # Keeps track of booked slots for the host to view

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']
    username = request.form['username']
    password = request.form['password']

    if user_type == 'host' and username == 'admin' and password == 'hostpass':
        session['user_type'] = 'host'
        return redirect(url_for('track_bookings'))
    elif user_type == 'client' and username == 'client' and password == 'clientpass':
        session['user_type'] = 'client'
        return redirect(url_for('book_slot'))
    else:
        return 'Invalid credentials, please try again.'

@app.route('/compare_hospitals')
def compare_hospitals():
    return render_template('compare_hospitals.html', hospitals=hospitals)

@app.route('/book_slot', methods=['GET', 'POST'])
def book_slot():
    if request.method == 'POST':
        client_name = request.form['client_name']
        hospital = request.form['hospital']
        time_slot = request.form['time_slot']
        
        # Save the booking information
        booked_slots.append({'client': client_name, 'hospital': hospital, 'time_slot': time_slot})
        return redirect(url_for('home'))
    
    return render_template('book_slot.html', hospitals=hospitals)

@app.route('/track_bookings')
def track_bookings():
    if session.get('user_type') == 'host':
        return render_template('track_bookings.html', bookings=booked_slots)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
