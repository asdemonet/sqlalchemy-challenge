import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement
Stations = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return (f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api.v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>"
            )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurements.date, Measurements.prcp).all()

    session.close()

    precipitation = list(np.ravel(results))

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Measurements.station).group_by(Measurements.station).all()

    session.close()

    stations = list(np.ravel(results))
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date > last_year).order_by(Measurements.date).all()

    session.close()

    temp_totals = []
    for result in temp:
        row = {}
        row["date"] = temp[0]
        row["tobs"] = temp[1]
        temp_totals.append(row)


    return jsonify(temp_totals)

@app.route("/api/v1.0/<start>")
def trip(date):
    session = Session(engine)

    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    last_year = dt.timedelta(days=365)

    start = start_date - last_year

    end = dt.date(2017, 8, 23)

    result = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()

    session.close()

    weather = list(np.ravel(result))
    
    return jsonify(weather)

@app.route("/api/v1.0/<start>/<end>")
def trip2(start, end):
    session = Session(engine)

    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    last_year = dt.timedelta(days=365)

    start = start_date - last_year

    end = end_date - last_year

    result = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()

    session.close()

    weather = list(np.ravel(result))
    
    return jsonify(weather)

if __name__ == "__main__":
    app.run(debug=True)