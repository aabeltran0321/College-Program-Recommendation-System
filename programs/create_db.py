import sqlite3
from sqlite3 import Error
class create_database(object):
    def __init__(self,filename):
        self.conn=self.create_connection(filename)

    def create_connection(self,db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file,check_same_thread=False)
            return conn
        except Error as e:
            print(e)
        return None
     
    def deleteUserByUsername(self,x):
        sql = 'DELETE FROM Users WHERE username=?'
        cur = self.conn.cursor()
        cur.execute(sql, (x,))
        self.conn.commit()   
    def delete_all_current_data(self):
        sql = 'DELETE FROM current_data'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        
    def GetDataFromTable(self,x):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM "+x)
        rows = cur.fetchall()
        return rows    
    def getDatabyUserPass(self,Username,Password):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM user WHERE username=? and password=?",(Username,Password))
        rows = cur.fetchall()
        return rows          
        
    def getQuestionsByCat(self,category):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM aptitude_test WHERE category=?",(category,))
        rows = cur.fetchall()
        return rows          
      
    def insertQuestion(self,category,question,choice_a,choice_b,choice_c,choice_d,correctanswer,pathtoimage):
        sql = ''' INSERT INTO aptitude_test(category,question,choice_a,choice_b,choice_c,choice_d,correctanswer,pathtoimage)
                  VALUES(?,?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (category,question,choice_a,choice_b,choice_c,choice_d,correctanswer,pathtoimage))
        self.conn.commit()
    
    def insertPurchases(self,controlNo,transaction1,timestamp,product,quantity,admin):
        sql = ''' INSERT INTO purchases(controlNo,transaction1,timestamp,product,quantity,admin)
                      VALUES(?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (controlNo,transaction1,timestamp,product,quantity,admin))
        self.conn.commit()  
    def insertReports(self,timestamp,product,inventory,quantity,expiration,user):
        sql = ''' INSERT INTO reports(timestamp,product,inventory,quantity,expiration,user)
                          VALUES(?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (timestamp,product,inventory,quantity,expiration,user))
        self.conn.commit()        
    def UpdateUser(self,ids,username,password):
        sql = ''' UPDATE Users
                      SET username = ? ,
                          password = ? 
                      WHERE id = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (username,password,ids))
        self.conn.commit()
    def UpdateProduct(self,code,title,brand,description,quantity,rop,roq,expire,price,category):
        sql = ''' UPDATE inventory
                          SET title = ? ,
                              brand = ? ,
                              description = ?,
                              quantity = ?,
                              rop = ?,
                              roq = ?,
                              expire = ?,
                              price = ?,
                              category = ?,
                              refqty = ?
                              
                          WHERE code = ?'''
        cur = self.conn.cursor()
        refqty=quantity
        cur.execute(sql, (title,brand,description,quantity,rop,roq,expire,price,category,refqty,code))
        self.conn.commit() 
    def UpdateQTTY(self,code,quantity):
        sql = ''' UPDATE inventory SET quantity = ? WHERE code = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (quantity,code))
        self.conn.commit()     
    def delete_product(self, code):
        sql = 'DELETE FROM inventory WHERE code=?'
        cur = self.conn.cursor()
        cur.execute(sql, (code,))
        self.conn.commit()            
if __name__ == '__main__':
    from aatk_module import NowToString
    conn = create_database("Database.db")
    
    for d in conn.GetDataFromTable("inventory"):
        print(d[1:(len(d)-1)])
    