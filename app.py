from re import L
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)
date_format = "%Y-%m-%d"

@app.route('/')
def index():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route('/api/v1.0/precipitation')
def prcp():
    session = Session(engine)
    prcp_list = []
    for date, prcp in session.query(Measurement.date,Measurement.prcp):
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)
    session.close()
    return jsonify(prcp_list)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    stat_list = []
    for stat,name,lat,lng,elev in session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all():
        stat_dict = {}
        stat_dict['station'] = stat
        stat_dict['name'] = name
        stat_dict['latitude'] = lat
        stat_dict['longitude'] = lng
        stat_dict['elevation'] = elev
        stat_list.append(stat_dict)
    session.close()
    return jsonify(stat_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    tobs_list = []
    latest_quer = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = datetime.datetime.strptime(latest_quer, date_format)
    search_date = datetime.datetime.date(latest_date.year - 1, latest_date.month, latest_date.day)
    for date, tobs in session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= search_date).all():
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs.dict)
    session.close()
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def search_start(start):
    session = Session(engine)
    search_list = []
    for min,avg,max in session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all():
        search_dict = {}
        search_dict['Min'] = min
        search_dict['Avg'] = avg
        search_dict['Max'] = max
        search_list.append(search_dict)
    session.close()
    return jsonify(search_list)

@app.route('/api/v1.0/<start>/<end>')
def search_start_stop(start,end):
    session = Session(engine)
    search_list = []
    for min,avg,max in session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all():
        search_dict = {}
        search_dict['Min'] = min
        search_dict['Avg'] = avg
        search_dict['Max'] = max
        search_list.append(search_dict)
    session.close()
    return jsonify(search_list)

if __name__ == "__main__":
    app.run(debug=True)