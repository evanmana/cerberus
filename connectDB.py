import pymysql.cursors


def connect():
    return  pymysql.connect('localhost', 'root', 'toor', 'cerberusDB')
