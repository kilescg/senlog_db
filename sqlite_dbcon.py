import sqlite3
import mysql.connector
from mysql.connector import Error

class db_connect():
    
    def __init__(self):
        
        self.conn_db = mysql.connector.connect(host="172.16.0.227", database='db_sde',user="admin",password="Banana-Pi00")
        
        try:
            if self.conn_db.is_connected():
                pass
                #print("database connect")
                # self.conn_db.cursor()
            else :
                print("No connect")
        except Error as e:
            print("Error while connecting to MySQL", e)
                    
    def aslist(self):
        
        return self.query_result
    
    def __iter__(self):
        return iter(self.aslist())
    
    def __str__(self):
        return str(self.result)
    
    def connect_select(self,table = None, condition = None ,field = None):
    
        try:
            cursor = self.conn_db.cursor()          
            if condition != None : 
               
                sqlite_select = f"SELECT {field} FROM {table} WHERE {condition}"
            
            else :
            
                sqlite_select = f"SELECT {field} FROM {table}"
            
            cursor.execute(sqlite_select)
            self.result = cursor.rowcount
            
            # if cursor.rowcount > 0 :
            self.query_result = cursor.fetchall()
                
            self.conn_db.commit()
            
        except sqlite3.Error as error :
            
            assert "Error while connecting to sqlite", error
            self.result = "error selete message: ",error
            
        finally :      
                 
            self.conn_db.close()         

    def connect_update(self,table = None ,values = None ,condition = None):
       
        try:     
            cursor = self.conn_db.cursor()
            sqlite_update = f"UPDATE {table} SET {values} WHERE {condition}" 
            cursor.execute(sqlite_update)
            self.conn_db.commit()
            self.result = "update successfully",table
            
        except sqlite3.Error as error :           
            assert "Error while connecting to sqlite", error
            # self.result = "error update massage: ",error
        finally :
            
            if self.conn_db:
                    self.conn_db.close()
            return cursor.rowcount     

    def connect_delete(self,table = None ,condition = None):

        try:
            
            cursor = self.conn_db.cursor()
            sqlite3_delect = f"DELETE FROM {table} WHERE {condition}"
            cursor.execute(sqlite3_delect)
            self.conn_db.commit()
            self.result = "delete successfully",table
            
        except sqlite3.Error as error :
            
            assert "Error while connecting to sqlite", error
            self.result = "error delete massage: ",error
        
        finally :
            if self.conn_db:
                    self.conn_db.close()

    def connect_sql_insert(self,table ,values):
        
        try:
            
            cursor = self.conn_db.cursor()                  
            sqlite_insert_query = f"INSERT INTO {table} VALUES {values}"
            cursor.execute(sqlite_insert_query)
            self.conn_db.commit()
            #print("Record inserted successfully into  table ", cursor.rowcount)
            cursor.close()
           
        except sqlite3.Error as error :
            
            assert "Error while connecting to sqlite", error
            self.result = "error insert  massage: ",error
           
        finally:           
            
            if self.conn_db:
                
                    self.conn_db.close()
                    #print("The SQLite connection is closed")
        
            return cursor.rowcount
    
    def connect_select_join(self,command):
    
        try:               
            cursor = self.conn_db.cursor()          
            sqlite_select = command
            cursor.execute(sqlite_select)
            self.query_result = cursor.fetchall()
            self.conn_db.commit()
            
        except sqlite3.Error as error :
            print("Error while connecting to sqlite", error)
            # assert "Error while connecting to sqlite", error
            self.result = "error selete message: ",error
            
        finally :        
            cursor.close()   
            self.conn_db.close()
            
        
         
