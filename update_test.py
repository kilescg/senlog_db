from sqlite_dbcon import db_connect
from utils import *
table = "db_sde.devices_income"
mac_id = "F4CE360FDD37AA0A"
note = "GOOD"
pm_1 = '27'
date_n_time = get_date_n_time()
time_n_date = get_time_n_date()


def test_select() :

    setID = []
    setAddress = []
    #===============================================================
    db_con = db_connect()
    db_con.connect_select("db_sde.sensor_income",None,"id_sensor")
    for id in db_con :
        setID.append(id[0])
    print(setID) 
    #===============================================================
    db_con = db_connect()
    db_con.connect_select("db_sde.sensor_income",None,"address")
    for address in db_con :
        print(date_n_time) 
        print(time_n_date)
        setAddress.append(address[0])
    print(setAddress) 
    #===============================================================
    id_max = len(setID)
    newID = id_max+1
    newID = str(newID)
    #===============================================================
    cnt = int(input('Enter a Adress : ')) 
    #========================== 
    sample0 = range(11, 20, 1)
    sample1 = range(21, 30, 1)
    sample2 = range(31, 40, 1)
    sample3 = range(41, 50, 1)
    #==========================
    if   cnt in sample0 :
        print("Test Sample 0")
    elif cnt in sample1 :
        print("Test Sample 1")
        pass
    elif cnt in sample2 :
        print("Test Sample 2")
        pass
    elif cnt in sample3 :
        print("Test Sample 3")
        pass
    else :
        print('"Out of Condition"')
        print(sample0)
    #===============================================================

def test_insert(newID) :

    sensor_table = "db_sde.sensor_income"
    data = "1300"
    model = "Sensirion SCD4x"
    date = get_datetime()
    val = "('"+newID+"','"+newID+"','"+model+"','"+data+"','"+date+"')"
    print(val)
    connect_insert = db_connect()
    connect_insert.connect_sql_insert(sensor_table,val)

def test_update() :

    value = "inspec_note = '"+note+"', pm_1 = '"+pm_1+"'"
    condition = "device_id = '"+mac_id+"'"
    connect_update = db_connect()
    connect_update.connect_update(table,value,condition)


if __name__ == "__main__":

    test_select()
    # test_insert()
    # test_update()