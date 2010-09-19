#!/usr/bin/env python
import sqlite3
import datetime
import time

def query_db_chartable(db_name, host, service, dateLimit):
	conn = sqlite3.connect(db_name)
	cursor = conn.cursor()
	sql_statement = """select value, time from data where host like ? and service like ? and time > ? order by time"""
	cursor.execute(sql_statement, (host, service, dateLimit) )
	results = cursor.fetchall()
	time_lable = [str(x[1]) for x in results]
	last = time_lable[int(len(time_lable) -1)]
	return results

def query_hosts_(db_name):
	conn = sqlite3.connect(db_name)
	cursor = conn.cursor()
	sql_statement = """select distinct host, service from data order by host"""
	cursor.execute(sql_statement)
	results = cursor.fetchall()
	return set(results)

def get_current_unix_time():
	return time.mktime(datetime.datetime.now().timetuple())

def subtract_one_week_worth_of_seconds(date):
	return date - (60 * 60 * 24 * 7)

if __name__ =="__main__":
	database_name = "/home/example/nit.db"
	output_dir = "/var/www/example-output/"

	hosts_s = query_hosts_(database_name)
	date_start = subtract_one_week_worth_of_seconds(get_current_unix_time())
	for host, service in hosts_s:
		results = query_db_chartable(database_name, host, service, date_start)
		if len(results) > 700:
			results = results[len(results) -567:]
		counts = [float(x[0]) for x in results if x[0] !=""]
		if counts == []:
			continue
		time_lable = [str(x[1]) for x in results]
		csv_output = "time,value"
		for time, count in zip(time_lable, counts):
			csv_output += "\n" + time + "," + str(count)
		f = open(output_dir + host + "-" + service + ".csv", "w")
		f.write(csv_output)
		f.close()

