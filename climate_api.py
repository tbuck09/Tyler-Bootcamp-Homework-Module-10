# Import dependencies
from flask import Flask, jsonify, request, render_template

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine= create_engine("sqlite:///Resources/hawaii.sqlite")

Base= automap_base()
Base.prepare(engine, reflect= True)

Measurement= Base.classes.measurement
Station= Base.classes.station

session= Session(engine)


#################################################
# Flask Setup
#################################################
app= Flask(__name__)


@app.route("/")
def root():
    print("Request made to Root")
    return (
        f"<h1>Welcome to Tyler Buck's Climate API!</h1><br/><i>This API focuses on stations located in Hawaii</i><br/>"
        "<br/>"
        f"<b>Available Routes:</b><br/>"
        f"<a href=\"http://127.0.0.1:5000/api/v1.0/precipitation\">Precipitation<br/></a>"
        f"<a href=\"http://127.0.0.1:5000/api/v1.0/stations\">Stations<br/></a>"
        f"<a href=\"http://127.0.0.1:5000/api/v1.0/tobs\">Temperature Observations<br/></a>"
        f"<a href=\"http://127.0.0.1:5000/api/v1.0/date_range\">Date Range<br/></a>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    print("Request made to Prcp")
    results= session.query(Measurement.station,Measurement.prcp).all()
    
    prcp_list = []
    for station, prcp in results:
        prcp_dict = {}
        prcp_dict["station"] = station
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def station():
    print("Request made to Station")
    results= session.query(Station.station).all()
    station_list= list(np.ravel(results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Request made to Tobs")
    results= session.query(Measurement.station,Measurement.date,Measurement.tobs).all()
    
    tobs_list = []
    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


@app.route("/api/v1.0/date_range")
def date_range_render():
    print("Request made to date_range")
    return render_template("test_form_html.html")

@app.route("/api/v1.0/date_range", methods=["POST"])
def date_range_post():
    print("Request made to Date_range_post")
    
    min_date_query= session.query(Measurement).order_by(Measurement.date).first()
    min_date= str(min_date_query.__dict__['date'])

    max_date_query= session.query(Measurement).order_by(Measurement.date.desc()).first()
    max_date= str(max_date_query.__dict__['date'])

    start= request.form["start"]
    end= request.form["end"]
    
    if start == "":
        start = min_date
    if end == "":
        end = max_date

    results= (session
        .query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
        )

    return (
        f"<h1>Minimum, Average, and Maximum Temperature for Date Range {start} through {end}</h1>"
        f"<b>Min Temp: </b>{results[0][0]}<br/>"
        "<b>Avg Temp: </b>"+"{:.2f}".format(results[0][1])+"<br/>"
        f"<b>Max Temp: </b>{results[0][2]}<br/>"
    )



@app.route("/api/v1.0/<start>")
def date_range_start_manual_url(start):
    print("Request made to Date_range_start_manual_url")

    max_date_query= session.query(Measurement).order_by(Measurement.date.desc()).first()
    max_date= str(max_date_query.__dict__['date'])
    
    end = max_date

    results= (session
        .query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
        )

    return (
        f"<h1>Minimum, Average, and Maximum Temperature for Date Range {start} through {end}</h1>"
        f"<b>Min Temp: </b>{results[0][0]}<br/>"
        "<b>Avg Temp: </b>"+"{:.2f}".format(results[0][1])+"<br/>"
        f"<b>Max Temp: </b>{results[0][2]}<br/>"
    )


@app.route("/api/v1.0/<start>/<end>")
def date_range_start_and_end_manual_url(start,end):
    print("Request made to Date_range_start_and_end_manual_url")

    results= (session
        .query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
        )

    return (
        f"<h1>Minimum, Average, and Maximum Temperature for Date Range {start} through {end}</h1>"
        f"<b>Min Temp: </b>{results[0][0]}<br/>"
        "<b>Avg Temp: </b>"+"{:.2f}".format(results[0][1])+"<br/>"
        f"<b>Max Temp: </b>{results[0][2]}<br/>"
    )

if __name__ == '__main__':
    app.run(debug=True)