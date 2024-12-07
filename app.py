from flask import Flask, render_template, request, redirect, url_for
from sql import save_profile, get_all_profiles, create_database,save_profiles

app = Flask(__name__)


@app.route('/')
def index():
    create_database()
    profiles = get_all_profiles()
    return render_template('index.html', profiles=profiles)


@app.route('/add', methods=['GET', 'POST'])
def add_profile():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        specialization = request.form['specialization']
        tsc_attended = request.form['tsc_attended']
        completion_year = request.form['completion_year']
        digital_address = request.form['digital_address']
        email = request.form['email']
        telephone = request.form['telephone']
        city = request.form['city']
        region = request.form['region']
        country = request.form['country']
        job_title = request.form['current_job_title']
        employer = request.form['current_employer']
        industry = request.form['industry_or_sector']
        save_profile(student_id,name, specialization, tsc_attended, completion_year, digital_address, email, telephone, city,
                     region, country,
                     job_title, employer, industry)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/import', methods=['GET', 'POST'])
def import_from_excel():
    """
    Imports profiles from a JSON payload, processes them, and saves them to the database.
    """
    data = request.get_json()
    profiles = data.get('profiles', [])

    profiles = [profile for profile in profiles if not all(v is None for v in profile)]

    profiles_to_insert = map_profiles_to_db_format(profiles)

    print(profiles_to_insert)

    saved = save_profiles(profiles_to_insert)

    return redirect(url_for('index'))



def map_profiles_to_db_format(profiles):
    """
    Maps profile data from the JSON structure to the database format.

    :param profiles: List of profile dictionaries from the JSON payload
    :return: List of tuples formatted for database insertion
    """
    return [
        (
            profile.get('ID', ''),       # Renamed key from 'ID' to 'Student ID'
            profile.get('Name', ''),
            profile.get('Specialization', ''),
            profile.get('TSC Attended', ''),
            profile.get('Completion Year', ''),
            profile.get('Digital Address', ''),
            profile.get('Email Address', ''),
            profile.get('Contact Number', ''),
            profile.get('City', ''),
            profile.get('Region', ''),
            profile.get('Country', ''),
            profile.get('Current Job Title', ''),
            profile.get('Current Employer', ''),
            profile.get('Current Industry', '')
        )
        for profile in profiles
    ]




if __name__ == '__main__':
    app.run(debug=True)
