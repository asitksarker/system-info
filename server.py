from flask import Flask, render_template, request
import db     

app = Flask(__name__)

@app.route('/')
def dashboard():
    # 1. Ask db.py for the latest records
    devices = db.get_latest_reports()
    
    # 2. Render templates/dashboard.html
    return render_template('dashboard.html', devices=devices)

@app.route('/history/<machine_id>')
def view_history(machine_id):
    # 1. Ask db.py for all reports for this specific machine
    history = db.get_history(machine_id)
    
    # 2. Render templates/history.html
    return render_template('history.html', machine_id=machine_id, history=history)

@app.route('/report', methods=['POST'])
def receive_report():
    data = request.json

    # 2. Save the data to SQLite
    db.save_report(data)
    
    return {"status": "success"}, 200

if __name__ == "__main__":
    db.init_db() # Ensure table exists
    app.run(host='0.0.0.0', port=5000, debug=True)