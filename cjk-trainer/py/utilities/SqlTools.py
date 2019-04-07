import sqlite3
import datetime
import sys

class SqlTools():
    def __init__(self, db_path):
        print("Opening database:" + db_path)
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
    def insertManyFromList(self, table_name, vocab_list):
        '''This function will insert a list's values and input them into a SQL database'''

        command = "INSERT INTO " + "[" + table_name + "] " + " (VOCABULARY, DEFINITION, PRONUNCIATION," \
                                                             " CORRECT, ATTEMPTED, STARRED) VALUES (?,?,?,?,?,?)"

        self.db.executemany(command, vocab_list)
        self.db.commit()
        self.setLastTimeStudied(table_name, date_time="min")

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
                   "STARRED BOOL,"
                   "VOCABULARY TEXT,"
                   "DEFINITION TEXT,"
                   "PRONUNCIATION TEXT,"
                   "CORRECT INT,"
                   "ATTEMPTED INT,"
                   "LASTTIMESTUDIED DATE);")

        # Extend table to include
        self.db.execute(command)
        self.db.commit()

        print("table ", table_name, " created!")

    def dropTable(self,table_name):
        command = "DROP TABLE " +"[" + table_name +"]"+ ";"
        self.db.execute(command)
        self.db.commit()

    def modifyTableRows(self, table_name, row_data, row_index):

        if self.validateRow(row_data):
            print("Table edit: ", row_data, " has been validated.")

            print("UPDATING TABLE DATA!", row_data)
            print("Updating table at card Num:", row_index)
            command = "UPDATE [" + table_name + "] SET STARRED=?, VOCABULARY=?, DEFINITION=?, PRONUNCIATION=?, " \
                                                            "CORRECT=?, ATTEMPTED=? WHERE CARDNUM= " + str(row_data.pop(0))
            print(command)
            self.db.execute(command, row_data)
            self.db.commit()
            print("Cardnum:", row_data[0], "has been modified.")

    def addTableRow(self, table_name, row_data):
        self.validateRow(row_data)

        command = "INSERT INTO " + "[" + table_name + "] " + " (STARRED, VOCABULARY, DEFINITION, PRONUNCIATION," \
                                                             " CORRECT, ATTEMPTED) VALUES (?,?,?,?,?,?)"
        print(command)
        self.db.execute(command, row_data[1:])
        self.db.commit()

    def deleteTableRow(self, table_name, row_index):
        command = "DELETE FROM " + "[" + table_name + "]" + " WHERE CARDNUM = " + row_index
        self.db.execute(command)
        self.db.commit()

    def validateRow(self, row_data):
        '''This function will check the data types of a list to make sure 1, 5, 6 are integers'''
        # TODO CHANGE LOGIC HERE PROBABLY
        # TODO COME BACK TO CHANGE THE INDEXES OF EACH ROW
        # The row being passed in will include everything including index 0, cardnum (primary key)
        # [CARDNUM ,STARRED, VOCABULARY, DEFINITION, PRONUNCIATION, CORRECT, ATTEMPTED, LASTTIMESTUDIED]
        if len(row_data) != 7:
            print("ERROR! Table edit: ", row_data, " has been REJECTED! Row length is ",len(row_data), ", should be 7.")
            return False
        #Im not sure I care if there is empty data in for words
        # elif row_data[2] == "" or row_data[3] == "" or row_data[4] == "":
        #     print("Empty critical slot found, refusing update into table")
        #     return False
        else:
            if row_data[1] != '0' and row_data[1] != '1':
                print("Resetting isStarred to 0")
                row_data[1] = '0'
            for i in range(5, 7):
                try:
                    row_data[i] = int(row_data[i])
                except ValueError:
                    print("VALUE ERROR: INTEGER FIELDS CANNOT CONTAIN A CHARACTER! RESETTING STATISTICS TO DEFAULT VALUES")
                    row_data[5] = '0'
                    row_data[6] = '0'
            print("Table edit: ", row_data, " has been validated.")
            return True



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

    def getTableList(self):
        # TODO SORT THE LIST BY DATE VALUE
        '''This function will return a list of tables inside of the database'''
        # queryCur = self.db.execute("SELECT * FROM sqlite_sequence")
        # result = queryCur.fetchall()
        # flat_list = []      # We don't need the number of entries in the table, just the name
        # for i in result:
        #     flat_list.append(i[0])
        #return flat_list
        cur = self.db.execute("SELECT NAME FROM sqlite_master WHERE type= " + "'table'" + " ORDER BY NAME;")
        result = cur.fetchall()
        flat_list = []      # We don't need the number of entries in the table, just the name
        for i in result:
            print(i)
            flat_list.append(i[0])

        print(flat_list)
        return flat_list

    def getTableData(self, table_name):
        '''This function will return a list of tuples representing the rows and columns of the table'''
        cur = self.db.execute("SELECT * FROM {}".format("[" + table_name + "]"))
        result = cur.fetchall()
        return result

    def setLastTimeStudied(self, table_name, date_time="now"):
        if date_time == "min":
            min = datetime.datetime.min
            iterList = [min]
            command = "UPDATE [" + table_name + "] SET LASTTIMESTUDIED = ?"
            self.db.execute(command, iterList)
            self.db.commit()

        elif date_time == "now":
            now = datetime.datetime.now()
            iterList =[now]
            command = "UPDATE [" + table_name + "] SET LASTTIMESTUDIED = ?"
            self.db.execute(command, iterList)
            self.db.commit()

    def getLastTimeStudied(self, table_name):
        print("TB", table_name)
        cur = self.db.execute("SELECT LASTTIMESTUDIED FROM [" + table_name + "];")
        result = cur.fetchone()

        try:
            result = result[0]
        except TypeError:
            result = '0'
        print(result)
        return result

    #TODO RETURN A LIST OF STARRED WORDS ONLY
    #def getStarredOnly(self):