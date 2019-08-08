# Log-Analysis

Udacity's Full Stack Web Development Nanodegree 1st Project


# Goal

Answers three important questions for a web server that has traffic stored in logs in the database and give insights about the access routines


# Requirements

* VirtualBox
* Vagrant
* Git
* Python 3
* PostgreSQL


# Steps to reproudce

1) download and install VirtualBox
2) download and install Vagrant
3) download [this](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) file that configures Vagrant to download an Ubuntu box, PostgreSQL, Python 3 and other dependecies...
4) open a shell terminal and run `vagrant up`
5) after the process is finished, run `vagrant ssh` to login to Ubuntu box
6) go to `\vagrant` using the command `cd \vagrant`, this folder is synced with the same vagrant folder in the configuration file you downloaded above
5) download the database creation commands from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
6) unzip and run `psql -d news -f newsdata.sql`, once finished, the database is already created and can be accessed normally
7) run the below views creations codes
8) run `python logs_analyser.py`
9) check the output against the uploaded `result.txt`


# Views

### Ratio calculator view
``` sql
CREATE VIEW rate AS
SELECT all.time,
       all.cnt AS olx,
       failure.cnt AS failedx,
       failure.cnt::double precision / all.cnt::double precision * 100 AS failRate
FROM failure, all
WHERE all.time = failure.time;
```

### Date accumulation
``` sql
CREATE VIEW total AS
SELECT time ::date, status
FROM log;
```

### Failed accumulation
``` sql
CREATE VIEW failure AS
SELECT time, count(*) AS cnt
FROM total
WHERE status = '404 NOT FOUND'
GROUP BY time;
```

### Success/failure accumulation
``` sql
CREATE VIEW all
SELECT time, count(*) AS cnt
FROM total
WHERE status = '200 OK'
OR
status = '404 NOT FOUND'
GROUP BY time;
```

# Tests
> PEP 8 Compatible code
