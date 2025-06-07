import psycopg2
from psycopg2.errors import UniqueViolation
from psycopg2.extensions import connection as Psycopg2Connection
from datetime import datetime

class DataBaseService():
    def __init__(self,host:str='localhost',database:str="mailbox", user:str="postgres", password:str="admin" ):
        try:
            self.conn=psycopg2.connect(
                host=host,
                database=database,       
                user=user,      
                password=password)
            self.curr=self.conn.cursor()
            self._ensure_tables()
        except psycopg2.Error as e:
            print("Failed to connect to the database:", e)
            raise

    def _close(self):
        self.curr.close()
        self.conn.close()

    def _ensure_tables(self):
        self.curr.execute("""
                          CREATE TABLE IF NOT EXISTS users
                          (id Bigserial PRIMARY KEY,
                          username VARCHAR(50) UNIQUE NOT NULL,
                          password_hash TEXT NOT NULL,
                          is_admin BOOL DEFAULT FALSE);
                           """)
        
        self.curr.execute("""
                          CREATE TABLE IF NOT EXISTS messages
                          (id Bigserial PRIMARY KEY,
                          receiver_id INTEGER REFERENCES users(id),
                          sender_id INTEGER REFERENCES users(id),
                          message VARCHAR(255) NOT NULL,
                          timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
                           """)
        self.conn.commit() 
    
    def _format_messages(self,id:int,sender:int,time:datetime,content):
        return f"""Message number:{id}\nfrom: {sender}\ntime: {time}\n{content}\n"""

    # def test(self):
    #     self.curr.execute(f"SELECT * FROM users")
    #     data=self.curr.fetchall()
    #     return data
    
    def create_user_check(self,username:str):
        self.curr.execute("""
    SELECT id FROM users WHERE username=(%s);""", (username,))
        result=self.curr.fetchone()
        if result:
            return None
        else: return True

    def create_user(self,username:str,password:str):
        try:
            self.curr.execute("""
        INSERT INTO users (username, password_hash) VALUES (%s,%s);""", (username,password))                                 
            self.conn.commit()   
            return (True, "User created")
        except UniqueViolation:
            self.conn.rollback()
            return (False, "User aready exists")
        except psycopg2.Error as e:
            self.conn.rollback()
            print("Database error:", e)
            return (False, "User cannot be created")

    def check_user(self,username:str):
        """
        Returns:
            Optional[Tuple[int, str, str]]: A tuple containing (id, username, password_hash) if the user exists,
            otherwise None.
                """
            
        self.curr.execute("""
    SELECT id, is_admin, password_hash FROM users WHERE username=(%s);""", (username,))
        result=self.curr.fetchone()
        if result:
            return (result)
        else: return (None)

    def password_change(self,id_user:int,password:str):
        """
        Returns:
            Optional Tuple(True, "Password updated successfully") if the password has been changed,
            otherwise Tuple (False, "Could not update password")
        """
        try:
            self.curr.execute("""
            UPDATE users SET password_hash =%s WHERE id=%s;""", (password,id_user))
            self.conn.commit()
            return (True, "Password updated successfully")
        except psycopg2.Error as e:
            self.conn.rollback()
            print("Database error:", e)
            return (False, "Could not update password")
        
    def get_id_by_user(self,username:str):
        """
        Returns: int or False if user not found
            """
        try:
            self.curr.execute("""SELECT id from users where username=%s;""",(username,))
            result=self.curr.fetchone()
            return result[0]
        except: return False
    
    def get_user_by_id(self,id:int):
        self.curr.execute("""SELECT username from users where id=%s;""",(id,))
        result=self.curr.fetchone()
        return result[0]

    def admin_all_users(self):
        self.curr.execute("""
    SELECT username FROM users;""",)
        result=self.curr.fetchall()
        if result:
            return (result)
        else: return (None)

    def msg_count(self,id_user:int):
        self.curr.execute("""
        SELECT COUNT(*) FROM messages WHERE receiver_id=%s;""",(id_user,))
        result=self.curr.fetchone()
        return (result[0])
    
    def load_message(self,id_reciver):
        """
        Input receiver_id
        Returns: list with messages for defined user if not found None
        """
        self.curr.execute("""
        SELECT 
        messages.id,
        us.username AS sender_name,
        ur.username AS receiver_name,
        messages.message,
        messages.timestamp
        FROM messages
        JOIN users AS us ON messages.sender_id = us.id
        JOIN users AS ur ON messages.receiver_id = ur.id
        WHERE ur.id=%s;
        """,(id_reciver,))

        data=self.curr.fetchall()
        result=[]
        for id,sender,receiver,content,time in data:
            time=time.strftime("%Y-%m-%d %H:%M:%S")
            message=self._format_messages(id,sender,content,time)
            result.append(message)
        return result
    

    def write_message(self,receiver:int,sender:int,content:str):
        """
        Inputs: receiver id,sender id ,content of message
        Returns:
           True if message is write in database,
            otherwise False
        """
        try:
            self.curr.execute("""
        INSERT INTO messages (receiver_id, sender_id,message) VALUES (%s,%s,%s);""", (receiver,sender,content))                                 
            self.conn.commit()   
            return True
        except: return False

    def delete_all_message(self,user:int):
        """
        Inputs: user id,
        Returns:
            Delete all messages for definied user
        """
        try:
            self.curr.execute("""
        DELETE FROM messages WHERE receiver_id=%s;""", (user,))                                 
            self.conn.commit()   
            return True
        except: return False

        
    def delete_one_message(self,id:int):
        """
        Inputs: id_message
        Returns:
            Delete the message with the given id 
        """
        try:
            self.curr.execute("""
        DELETE FROM messages WHERE id=%s;""", (id,))                                 
            self.conn.commit()   
            return True
        except: return False





