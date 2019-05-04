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

min_date_query= session.query(Measurement).order_by(Measurement.date).first()
min_date= str(min_date_query.__dict__['date'])

max_date_query= session.query(Measurement).order_by(Measurement.date.desc()).first()
max_date= str(max_date_query.__dict__['date'])

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
        f"<a href=\"http://127.0.0.1:5000/api/v1.0/precipitation\" target=\"_blank\">Precipitation<br/></a>"
        f"<a href=\"http://127.0.0.1:5000/api/v1.0/stations\" target=\"_blank\">Stations<br/></a>"
        f"<a href=\"http://127.0.0.1:5000/api/v1.0/tobs\" target=\"_blank\">Temperature Observations<br/></a>"
        f"<a href=\"http://127.0.0.1:5000/api/v1.0/date_range\" target=\"_blank\">Date Range<br/></a>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    print("Request made to Prcp")
    session= Session(engine)
    results= session.query(Measurement.date,Measurement.prcp).all()
    
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def station():
    print("Request made to Station")
    session= Session(engine)
    results= session.query(Station.station).all()
    station_list= list(np.ravel(results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Request made to Tobs")
    session= Session(engine)
    results= (session
                .query(Measurement.date,Measurement.tobs)
                .filter(Measurement.date >= min_date)
                .filter(Measurement.date <= max_date)
                .all())
    
    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


@app.route("/api/v1.0/date_range")
def date_range_render():
    print("Request made to Date_range_render")
    return render_template("date_range_form.html")

@app.route("/api/v1.0/date_range", methods=["POST"])
def date_range_post():
    print("Request made to Date_range_post")
    
    session= Session(engine)

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
        f"<h1>Minimum, Average, and Maximum Temperature for Date Range:</h1>"
        f"<h2>{start} through {end}</h2>"
        f"<b>Min Temp: </b>{results[0][0]}<br/>"
        "<b>Avg Temp: </b>"+"{:.2f}".format(results[0][1])+"<br/>"
        f"<b>Max Temp: </b>{results[0][2]}<br/>"
    )



@app.route("/api/v1.0/<start>")
def date_range_start_manual_url(start):
    print("Request made to Date_range_start_manual_url")

    session= Session(engine)
    
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
        f"<h1>Minimum, Average, and Maximum Temperature for Date Range:</h1>"
        f"<h2>{start} through {end}</h2>"
        f"<b>Min Temp: </b>{results[0][0]}<br/>"
        "<b>Avg Temp: </b>"+"{:.2f}".format(results[0][1])+"<br/>"
        f"<b>Max Temp: </b>{results[0][2]}<br/>"
    )


@app.route("/api/v1.0/<start>/<end>")
def date_range_start_and_end_manual_url(start,end):
    print("Request made to Date_range_start_and_end_manual_url")

    session= Session(engine)
    
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
        f"<h1>Minimum, Average, and Maximum Temperature for Date Range:</h1>"
        f"<h2>{start} through {end}</h2>"
        f"<b>Min Temp: </b>{results[0][0]}<br/>"
        "<b>Avg Temp: </b>"+"{:.2f}".format(results[0][1])+"<br/>"
        f"<b>Max Temp: </b>{results[0][2]}<br/>"
    )


if __name__ == '__main__':
    app.run(debug=True)