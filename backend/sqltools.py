import pymysql
pymysql.install_as_MySQLdb()
from web import models

def select(host, port, user, pwd, sql, database):
    conn = pymysql.connect(host=host, port=port, user=user, password=pwd, database=database)
    cursor = conn.cursor()
    base_sql = "select * from (%s) as wb limit 0,50;"
    cursor.execute(sql)
    column_list = cursor.description
    column_list = [column[0] for column in column_list]
    result = {}
    result['column_list'] = column_list
    value_list = cursor.fetchall()
    value_list2 = []
    for value in value_list:
        value = [str(i) for i in value]
        value_list2.append(value)
    result['value_list'] = value_list2
    cursor.close()
    conn.close()
    return result


def select_database(host, port, user, pwd):
    conn = pymysql.connect(host=host, port=port, user=user, password=pwd)
    cursor = conn.cursor()
    base_sql = "show databases;"
    cursor.execute(base_sql)
    result = cursor.fetchall()
    sec_db_list = models.SecretDB.objects.all()
    result2 = []
    for i in result:
        flag = 1
        for sec_db in sec_db_list:
            if sec_db.name == i[0]:
                flag = 0
        if flag == 1:
            result2.append(i)
    cursor.close()
    conn.close()
    return result2
