from flask import Flask, render_template, jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

app = Flask(__name__)

# Fixed date of birth (07 January 2000)
fixed_dob_str = "07012000"

def calculate_time_left(dob_str):
    """
    Calculate the remaining time from the current date until the user turns 70 years old
    based on their given date of birth.
    """
    try:
        # Convert the date string to a datetime object
        dob = datetime.strptime(dob_str, "%d%m%Y")
    except ValueError:
        return None  # Return None if the date format is incorrect

    # Set maximum age to 70 years
    max_age = 70  # maximum age in years
    end_date = dob + relativedelta(years=max_age)  # Adding 70 years to dob

    today = datetime.now()

    if today >= end_date:
        return {"message": "You've reached or surpassed the age of 70!"}

    # Calculate the remaining time
    remaining_time = end_date - today
    remaining_seconds_total = int(remaining_time.total_seconds())

    # Calculate years, months, weeks, days
    remaining_years = remaining_time.days // 365
    remaining_months = (remaining_time.days // 30)  # Approximate months
    remaining_weeks = remaining_time.days // 7
    remaining_days = remaining_time.days  # Remaining total days

    # Total hours, minutes, seconds
    total_hours = remaining_seconds_total // 3600
    total_minutes = remaining_seconds_total // 60
    seconds = remaining_seconds_total % 60

    # Calculate year progress
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    end_of_year = datetime(now.year, 12, 31)
    total_days_in_year = (end_of_year - start_of_year).days + 1  # Including 31st Dec
    days_passed = (now - start_of_year).days
    year_progress = (days_passed / total_days_in_year) * 100  # Percentage of year passed

    return {
        "seconds": remaining_seconds_total,
        "minutes": f"{total_minutes}:{seconds:02}",
        "hours": f"{total_hours}:{total_minutes % 60:02}:{seconds:02}",
        "weeks": remaining_weeks,
        "months": remaining_months,
        "years": remaining_years,
        "days": remaining_days,
        "year_progress": year_progress,
        "current_year": now.year,
        "current_month": calendar.month_name[now.month],
        "days_left_in_month": (calendar.monthrange(now.year, now.month)[1] - now.day),
        "hours_left_in_day": (24 - now.hour)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time_left')
def time_left():
    result = calculate_time_left(fixed_dob_str)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Invalid date format."}), 400

if __name__ == '__main__':
    app.run(debug=True)
