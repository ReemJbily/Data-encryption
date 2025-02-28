import psycopg2

class DataBase:
    '''
    this class responsible for establishing a database conection
    and all necessary methods to save and read a file from the database
    '''
    def __init__(self):
         self.conn = psycopg2.connect(
         database="filedata", user='postgres', password='1234', host='127.0.0.1', port= '5432')

         self.cursor = self.conn.cursor()
         
    def insertValues(self,fileName,content):
        self.cursor.execute('''INSERT INTO FILES_TABLE (filename, content) VALUES (%s, %s)''', (fileName,content))        
        self.conn.commit()
    def readFile(self):
        self.cursor.execute('''SELECT content FROM files_table ORDER BY id DESC LIMIT 1''')
        self.conn.commit()
        return self.cursor.fetchall()
    def deleteContent(self):
        self.cursor.execute('''DELETE FROM files_table''')
        self.conn.commit()