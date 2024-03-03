# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
station = base.classes.station
measurement = base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app =Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary using date as the key and prcp as the value."""
    # Calculate the date one year from the last date in the dataset
    latest_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Query temperature observations of the most-active station for the previous year of data."""
    # Find the most active station
    most_active_station = session.query(measurement.station).group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()

    if most_active_station:
        most_active_station_id = most_active_station[0]

        # Calculate the date one year from the last date in the dataset
        latest_date = session.query(func.max(measurement.date)).scalar()
        
        one_year_ago = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
        session.close()
        # Query temperature observations for the most active station for the previous year
        results = session.query(measurement.date, measurement.tobs).\
            filter(measurement.station == most_active_station_id).\
            filter(measurement.date >= one_year_ago).all()
        session.close()
        # Convert the query results to a list of dictionaries
        tobs_data = [{"date": date, "temperature": tobs} for date, tobs in results]

        return jsonify(tobs_data)

 

@app.route("/api/v1.0/<start>")
def start_date_stats(start):
    """Calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
    # Query temperature statistics for the specified start date
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()
    # Convert the query results to a dictionary
    stats_data = {
        "temp_min": results[0][0],
        "temp_avg": results[0][1],
        "temp_max": results[0][2]
    }

    return jsonify(stats_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date_stats(start, end):
    """Calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""
    # Query temperature statistics for the specified date range
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
if __name__ == '__main__':
    app.run()