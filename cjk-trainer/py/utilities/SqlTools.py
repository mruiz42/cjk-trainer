import sqlite3
import sys

class SqlTools():
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)
        self.cur = self.db.cursor()

    def createDatabase(self):
        print("foo")

    # def openDatabase(self, dbname):
    #     #check if already open
    #     self.db = sqlite3.connect(dbname)
    #     self.cur = self.db.cursor()
    #     return self.cur

    def closeDatabase(self):
        #print("something")
        self.db.close()

    #TODO ADD FIELDS/REARRANGE
    def insertVocabWordList(self, table_name, headers, vocabword_list):
        header_string = '(' + ', '.join(headers + ['STARRED', 'CORRECT', 'ATTEMPTED', 'LASTTIMESTUDIED']) + ')'
        placeholders = '(' + ', '.join(['?' for header in headers] + ['0', '0', '0', '0']) + ')'
        command = "INSERT INTO " + "[" + table_name + "]" + header_string + " VALUES " + placeholders
        print(command)
        self.db.executemany(command, vocabword_list)
        self.db.commit()

    def createTable(self, table_name):
        #c = self.db.cursor()
        #c = self.cur
        # Check if table exists
        # try:
        #     c.execute('SELECT * FROM ' + tablename)
        #     print(c.fetchall())
        #     print("table exists, probably.")
        # except sqlite3.OperationalError:
        #     # Table must not exist
        #     # SEARCH FOR TABLE NAME AND DONT RUN IF FOUND!
        command = ("CREATE TABLE IF NOT EXISTS [" + str(table_name) + "] "
                   "(CARDNUM INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "STARRED INT,"
                   "VOCABULARY CHAR,"
                   "DEFINITION CHAR,"
                   "PRONUNCIATION CHAR,"
                   "CORRECT INT,"
                   "ATTEMPTED INT,"
                   "LASTTIMESTUDIED CHAR);")

        # Extend table to include
        self.db.execute(command)
        self.db.commit()
        print("table ", table_name, " created!")

    def dropTable(self,table_name):
        command = "DROP TABLE " +"[" + table_name +"]"+ ";"
        self.db.execute(command)
        self.db.commit()

    def modifyTableRows(self, table_name, row_data, row_index):
        if row_data[0] == "" or row_data[2] == "" or row_data[3] == "":
            print("Empty critical slot found, refusing update into table")
        else:
            self.checkUserTableEdit(row_data)
            print("UPDATING TABLE DATA!", row_data)
            print("Updating table at card Num:", row_index)

            command = "UPDATE " + table_name + " SET VOCABULARY=?, DEFINITION=?, PRONUNCIATION=?, " \
                                                            "ATTEMPTED=?, CORRECT=?, STARRED=? " \
                                                            " WHERE CARDNUM= " + str(row_data.pop(0))
            print(command)
            self.db.execute(command, row_data)
            self.db.commit()

    def addTableRow(self, table_name, row_data):
        self.checkUserTableEdit(row_data)

        command = "INSERT INTO " + "[" + table_name + "] " + " (VOCABULARY, DEFINITION, PRONUNCIATION," \
                                                "ATTEMPTED, CORRECT, STARRED) VALUES (?,?,?,?,?,?)"
        print(command)
        self.db.execute(command, row_data)
        self.db.commit()

    def deleteTableRow(self, table_name, row_index):
        command = "DELETE FROM " + "[" + table_name + "]" + " WHERE CARDNUM = " + row_index
        self.db.execute(command)
        self.db.commit()

    def checkUserTableEdit(self, row):
        '''This function will check the data types of a list to make sure 0, 4, 5, 6 are integers'''
        # THIS LOGIC IS FLAWED UNLESS YOU CHECK FOR A LEN6 AND LEN7 LIST
        # TODO CHANGE LOGIC HERE PROBABLY
        # TODO COME BACK TO CHANGE THE INDEXES OF EACH ROW
        try:
            row[0] = int(row[0])
        except ValueError:
            print("FATAL ERROR, PRIMARY KEY HAS BEEN EDITED!")
            return False
        if row[1] != 0 and row[1] != 1:
            print("Resetting isStarred to 0")
            row[1] = 0
        indexesToConvert = [4, 5, 6]
        for i in indexesToConvert:
            try:
                row[i] = int(row[i])
            except ValueError:
                print("VALUE ERROR: INTEGER FIELDS CANNOT CONTAIN A CHARACTER! RESETTING STATISTICS TO DEFAULT VALUES")
                row[4] = 0
                row[5] = 0
                # row[i] = 0


    #TODO MULTIPLE LANG SUPPORT
    def findVocab(self, hanzi):
        self.cur.execute("SELECT * FROM TEST WHERE HANZI = ?", (hanzi,))
        data= self.cur.fetchall()
        if len(data)==0:
            print('There is no component named %s'%hanzi)
        else:
            print('Component %s found with rowids %s'%(hanzi,','.join(map(str, next(zip(*data))))))

    def consolidateEntries(self):
        #I guess multiple words can have sepeate defintions and pronunciations, so look for words that only have
        # are completely identical meaning same hanzi, pinyin, definition.
        print("I guess find any conflicting entries(same hanzi) and then merge the definitions")


    # TODO
    #  When I inserted into the table before, I had a typo where it had no comma after PRONUNCIATION in the query,
    #  and it was complaining about 7 values being passed to the command because the hidden cardnum cell was still there
    # TODO CHANGE THIS FOR MULTIPLE LANG SUPPORT
    def CSVtoSQLDatabase(self, csvfile, tablename):
        '''This function will parse a CSV line where format is as follows:
        vocabulary word,pronunciation,definition1;definition2;etc.
        (hanzi),(pinyin),(English defn.)'''

        hanzi = ""
        pinyin = ""
        definition = ""
        file = open(csvfile, mode="r")
        self.createTable(tablename)

        #cardnum = 0
        for line in file:
            if (len(line) == 0):
                print("Empty Line!")
            elif (line[0] == '#'):
                print("Comment line!")
            else:
                pos0 = line.find(",")
                pos1 = line.find(",", pos0 + 1)
                hanzi = line[0:pos0]
                pinyin = line[pos0 + 1:pos1]
                definition = line[pos1 + 1:-1]
                tup = [(hanzi, pinyin, definition,0,0,0)]
                print(tup)
                self.cur.executemany('INSERT OR IGNORE INTO ' + tablename +
                                     '(HANZI, PINYIN, DEFINITION, STARRED, ATTEMPTED, CORRECT) VALUES (?,?,?,?,?,?)'
                                     , tup)
                #cardnum += 1
        file.close()
        self.db.commit()
        print("Finished importing", self.db.total_changes, "entries.")
