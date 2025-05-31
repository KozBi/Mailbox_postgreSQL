import psycopg2

class DataBaseService():
    def __init__(self,host:str='localhost',database:str="test", user:str="postgres", password:str="admin" ):
        self.conn=psycopg2.connect(
            host=host,
            database=database,       
            user=user,      
            password=password)
        self.curr=self.conn.cursor()

    def _close(self):
        self.curr.close()
        self.conn.close()


    def test(self):
        self.curr.execute("SELECT * FROM person;")
        data=self.curr.fetchall()
        self._close() 
        return data

