# sqlalchemy-challenge
In this project, I utilized SQLAlchemy in Jupyter Notebook and Flask in VS Code to build a climate analysis and exploration API for a SQLite database containing weather data for Hawaii. The two csv files that contained data were Hawaii measurements and Hawaii stations. I began by setting up the database engine and reflecting the existing tables using automap_base. I then created a Flask application with different routes to perform specific queries. The routes included precipitation data for the last 12 months, listing available weather stations, querying temperature observations for the most active station, and calculating temperature statistics for specified date ranges. There were nine stations and the most active station was USC00519281 with Lowest Temperature: 54.0, Highest Temperature: 85.0, and Average Temperature: 71.66. I had to hard code the date for one year ago at the suggestion of my professor because I kept getting an error with dt. Our data returned the following information. 
count	2230	2021.000000
mean	2017-02-16 05:31:15.874439424	0.177279
min	2016-08-23 00:00:00	0.000000
25%	2016-11-18 00:00:00	0.000000
50%	2017-02-14 12:00:00	0.020000
75%	2017-05-17 00:00:00	0.130000
max	2017-08-23 00:00:00	6.700000
std	NaN	0.461190
![image](https://github.com/kelseajade/sqlalchemy-challenge/assets/152021966/1a0e5697-9fc3-457f-a5bc-006532d6b5d0)
I used Matplotlib to visualize temperature observations through histograms. 
![image](https://github.com/kelseajade/sqlalchemy-challenge/assets/152021966/5bcb963d-6e94-4943-a3c2-2caeab07fcce)
The Flask API allows users to access and analyze the given climate data for Hawaii. I used AskBCS for help with getting my flask to run. I needed to add if __name__ == '__main__':
    app.run() to the end. He also suggested I add "session.close()" after each query. 
