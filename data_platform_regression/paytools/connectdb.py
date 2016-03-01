__author__ = 'whuyi123'
import MySQLdb
import os,sys

def db_connect(dbhost,dbport,dbuser,dbpwd,dbname):
    try:
        # Open database connection
        db = MySQLdb.connect(host=dbhost,port=int(dbport),user=dbuser,passwd=dbpwd,db=dbname,charset='utf8')
        print "db connection successfully"
    except:
        print "db connectiong fail"
        sys.exit(-1)
    return db

def db_op(sql, db_ins):

    # prepare a cursor object using cursor() method
    cursor = db_ins.cursor()
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db_ins.commit()
        rows=cursor.fetchall()
        print "sql execute successfully"
    except:
        # Rollback in case there is any error
        db_ins.rollback()
    return rows
