from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
db = SQLAlchemy(app)

class MyTable(db.Model):
    __tablename__ = 'reports'
    report_number = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String)
    report_classification = db.Column(db.String)
    season = db.Column(db.String)
    state = db.Column(db.String)
    month_number = db.Column(db.String)
    submitted_by = db.Column(db.String)
    year = db.Column(db.String)
    month = db.Column(db.String)
    day = db.Column(db.String)
    county = db.Column(db.String)
    location_details = db.Column(db.String)
    nearest_town = db.Column(db.String)
    nearest_road = db.Column(db.String)
    observed = db.Column(db.String)
    also_noticed = db.Column(db.String)
    other_witnesses = db.Column(db.String)
    environment = db.Column(db.String)
    other_stories = db.Column(db.String)
    time_and_conditions = db.Column(db.String)
    follow_up = db.Column(db.String)
    follow_up_details = db.Column(db.String)
    day_of_week = db.Column(db.String)
    date = db.Column(db.String)
    submitted_by_date = db.Column(db.String)

@app.route('/')
def index():
    states = [state[0] for state in db.session.query(MyTable.state.distinct()).order_by(MyTable.state).all()]
    states.insert(0, 'All')  
    report_classifications = [classification[0] for classification in db.session.query(MyTable.report_classification.distinct()).order_by(MyTable.report_classification).all()]
    report_classifications.insert(0, 'All') 
    seasons = [season[0] for season in db.session.query(MyTable.season.distinct()).order_by(MyTable.season).all()]
    seasons.insert(0, 'All')  
    years = [year[0] for year in db.session.query(MyTable.year.distinct()).order_by(MyTable.year).all()]
    years.insert(0, 'All')  
    counties = [county[0] for county in db.session.query(MyTable.county.distinct()).order_by(MyTable.county).all()]
    counties.insert(0, 'All')  
    return render_template('index.html', states=states, report_classifications=report_classifications, seasons=seasons, years=years, counties=counties)


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        selected_state = request.form['state']
        selected_classification = request.form['report_classification']
        selected_season = request.form['season']
        selected_year = request.form['year']
        selected_county = request.form['county']
        
        query = MyTable.query
        
        if selected_state != 'All':
            query = query.filter_by(state=selected_state)
        
        if selected_classification != 'All':
            query = query.filter_by(report_classification=selected_classification)
        
        if selected_season != 'All':
            query = query.filter_by(season=selected_season)
        
        if selected_year != 'All':
            query = query.filter_by(year=selected_year)
        
        if selected_county != 'All':
            query = query.filter_by(county=selected_county)
        
        data = query.all()
        
        return render_template('data.html', data=data)
    else:
        data = MyTable.query.all()
        return render_template('data.html', data=data)

from flask import jsonify

@app.route('/get_record_count', methods=['GET', 'POST'])
def get_record_count():
    if request.method == 'POST':
        selected_state = request.form['state']
        selected_classification = request.form['report_classification']
        selected_season = request.form['season']
        selected_year = request.form['year']
        selected_county = request.form['county']
        
        query = MyTable.query
        
        if selected_state != 'All':
            query = query.filter_by(state=selected_state)
        
        if selected_classification != 'All':
            query = query.filter_by(report_classification=selected_classification)
        
        if selected_season != 'All':
            query = query.filter_by(season=selected_season)
        
        if selected_year != 'All':
            query = query.filter_by(year=selected_year)
        
        if selected_county != 'All':
            query = query.filter_by(county=selected_county)
        
        record_count = query.count()
        
        return jsonify({'total_records': record_count})
    elif request.method == 'GET':
        return jsonify({'message': 'Method not allowed'}), 405
    else:
        return jsonify({'message': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True)
