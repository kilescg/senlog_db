from sqlite_dbcon import db_connect
from utils import *

cal_con = db_connect()
cal_tab = "db_sde.sensor_farformhome"
dt_string = get_datetime()
cnt = 1
address = 11
model = "SCD41"
targeted_data = 1111.101
cal_val = "('"+str(dt_string)+"','"+str(cnt)+"','"+str(address)+"','"+str(model)+"','"+str(targeted_data)+"')"
print(cal_val)
cal_con.connect_sql_insert(cal_tab,cal_val)
