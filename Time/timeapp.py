from flask import Flask, render_template, jsonify, request
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

def calculate_time_left(dob_str):
    """
    Calculate the remaining time from the current date until the user turns 70 years old
    based on their given date of birth.
    """
    try:
        # Ensure the date format is in DDMMYYYY (e.g., '07012000')
        dob = datetime.strptime(dob_str, "%d%m%Y")
    except ValueError:
        return None  # Return None if the date format is incorrect

    # Set maximum age to 70 years
    max_age = 70  # maximum age in years
    end_date = dob + relativedelta(years=max_age)  # Adding 70 years to dob

    today = datetime.now()

    if today >= end_date:
        return {"message": "You've reached or surpassed the age of 70!"}

    # Calculate the remaining time using relativedelta for better accuracy
    remaining_time = relativedelta(end_date, today)
    
    # Total days and seconds calculations
    remaining_days = (end_date - today).days
    remaining_seconds_total = int((end_date - today).total_seconds())

    # Calculate total hours, minutes, and seconds
    total_hours = remaining_seconds_total // 3600
    total_minutes = remaining_seconds_total // 60
    seconds = remaining_seconds_total % 60

    return {
        "seconds": remaining_seconds_total,
        "minutes": f"{total_minutes}:{seconds:02}",
        "hours": f"{total_hours}:{total_minutes % 60:02}:{seconds:02}",
        "weeks": remaining_days // 7,
        "months": remaining_time.months + remaining_time.years * 12,  # Total months
        "years": remaining_time.years,
        "days": remaining_days
    }

@app.route('/')
def index():
    return render_template('indexx.html')

@app.route('/time_left/<dob_str>', methods=['GET'])
def time_left(dob_str):
    # Validate the date format, it should be DDMMYYYY (e.g., '07012000')
    if len(dob_str) != 8 or not dob_str.isdigit():
        return jsonify({"error": "Invalid date format. Please enter in DDMMYYYY format."}), 400
    
    result = calculate_time_left(dob_str)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Invalid date format. Please enter in DDMMYYYY format."}), 400

if __name__ == '__main__':
    app.run(debug=True)
