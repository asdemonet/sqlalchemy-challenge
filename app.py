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
            f"/api.v1.0/temperature<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start><end><br/>"
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

@app.route("/api/v1.0/temperature")
def tobs():
    session = Session(engine)

    results = session.query(Measurements.date, Measurements.tobs).filter((Measurements.station) == "USC00519281").all()

    session.close()

    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start():
    return 

@app.route("/api/v1.0/<start><end>")
def start_end():
    return 

if __name__ == "__main__":
    app.run(debug=True)