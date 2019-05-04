# Practice with SQLAlchemy and Flask Apps

This homework focuses on two parts: The first section manipulates a sqlite database using **SQLAlchemy** in a python notebook (climate_starter.ipynb). The second section also employs SQLAlchemy, but focuses on using **Flask** to deliver the data in a JSON format via the web.

## climate_starter.ipynb
* After importing dependencies, we _reflect_ the sqlite database in order to make our lives easier when working with the file.
* The first query explores data over the course of the last year (of the data provided: 2016-08-23). This is saved in a Pandas DataFrame and plotted using Matplotlib.
* The following query seeks to count the number of observations made by each Station using SQLAlchemy _joins_ and _group\_bys_. The station with the most observations made (USC00519281) and plots the Observed Temperatures (tobs) to a histogram.
* Next, using a hypothetical starting date (2017-08-01) for a lovely Hawaii rendezvous, we calculate the minimum, average, and maximum of temperatures over the last year since the start date. The average is plotted as a bar chart with an "error bar" produced from the difference between the max and min temperature values.
* The notebook concludes with a variation of the previous query: We plot the minimum, average, and maximium for the hypothetical Hawaii holiday _throughout the years_ (August 01 - 08 from 2010-2017) and plot these as an area chart.

## climate_api.py
* Again we import dependencies and quickly prepare our SQLAlchemy objects for further querying in the webpages created using flask.
* After initializing the Flask app object, the _Root_ is defined. This landing page will direct users to any information about the database their heart desires - within reason, of course.
* The _Precipitation_ page presents the user with each date and the precipitation observed in a JSON format.
* The _Stations_ page does the same, but only presenting the stations from with this data was derived.
* _Temperature Observations_ follows suit, presenting the date and temperature observations.
* The _Date Range_ page is a light practice with HTML forms.
    * Using the _Date Range_ link from the landing page will take the user to a UI from which they can enter their own start and end dates. This will return the minimum, average, and maximum for the date range provided in a JSON format.
    * An alternative method is listed which informs the user of how the same results can be achieved by providing the start and end dates in the URL.
        * Note: Should the user provide only one date, this returns the same information starting from the date provided and ending with the last date in the database (2017-08-23).