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

    def closeDatabase(self):
        print("Database will now close...")
        self.db.close()

    def createCardsTable(self):
        command =  ("CREATE TABLE IF NOT EXISTS CARDS "
                    "(CARD_ID INTEGER PRIMARY KEY AUTOINCREMENT,"           # Card Identification number
                    "DECK_ID TEXT NOT NULL,"                                # Deck name of cards being studied
                    "IS_STARRED BOOLEAN,"
                    "VOCABULARY TEXT,"                                      # Vocabulary in secondary language
                    "DEFINITION TEXT,"                                      # Definition in primary language
                    "PRONUNCIATION TEXT,"                                   # Pronunciation of secondary language
                    "IMAGE_DATA BLOB,"
                    "FOREIGN KEY(DECK_ID) REFERENCES DECKS(DECK_ID));")     # Flag for word
        self.db.execute(command)
        self.db.commit()

    def createDeckTable(self):
        command = ("CREATE TABLE IF NOT EXISTS DECKS "
                   "(DECK_ID TEXT PRIMARY KEY,"
                   "VOCABULARY_LANGUAGE TEXT,"
                   "DEFINITION_LANGUAGE TEXT);")
        self.db.execute(command)
        self.db.commit()

    def createSessionsTable(self):
        command = ("CREATE TABLE IF NOT EXISTS SESSIONS"
                   "(START_TIME DATE PRIMARY KEY,"
                   "DECK_ID TEXT, "
                   "FOREIGN KEY(DECK_ID) REFERENCES DECKS(DECK_ID));")
        self.db.execute(command)
        self.db.commit()

    def createStatisticsTable(self):
        command = ("CREATE TABLE IF NOT EXISTS STATISTICS"
                   "(CARD_ID INTEGER,"
                   "DECK_ID TEXT,"
                   "START_TIME DATE,"
                   "TIMES_CORRECT INTEGER,"
                   "TIMES_ATTEMPTED INTEGER,"
                   "FOREIGN KEY(CARD_ID) REFERENCES CARDS(CARD_ID),"
                   "FOREIGN KEY(DECK_ID) REFERENCES DECKS(DECK_ID),"
                   "FOREIGN KEY(START_TIME) REFERENCES SESSIONS(START_TIME));")
        self.db.execute(command)
        self.db.commit()

    def createLanguagesTable(self):
        command = ("CREATE TABLE IF NOT EXISTS LANGUAGES"
                   "(LANGUAGE_NAME TEXT,"
                   "STARRED BOOLEAN);")
        self.db.execute(command)
        self.db.commit()

    def insertCard(self, rows):
        '''tuple: (DECK_ID, VOCABULARY, DEFINITION, PRONUNCIATION)'''
        # command = "INSERT INTO CARDS VALUES(DECK_ID=?, VOCABULARY=?, DEFINITION=?, PRONUNCIATION=?, IS_STARRED=FALSE);"
        command = "INSERT INTO CARDS (DECK_ID, IS_STARRED, VOCABULARY, DEFINITION, PRONUNCIATION, IMAGE_DATA)VALUES(?,?,?,?,?,NULL)"
        self.db.execute(command, rows)
        self.db.commit()

    def insertDeck(self, deck_name, vocabulary_language, definition_language):
        t = (deck_name, vocabulary_language, definition_language)
        command = ("INSERT INTO DECKS VALUES(?, ?, ?);")
        self.db.execute(command, t)
        self.db.commit()

    def insertManyCards(self, tuple_List):
        '''List:Tuple: [(DECK_ID, VOCABULARY, DEFINITION, PRONUNCIATION, IS_STARRED), ...]'''
        command = "INSERT INTO CARDS (DECK_ID, VOCABULARY, DEFINITION, PRONUNCIATION, IS_STARRED) VALUES (?,?,?,?,?)"
        self.db.executemany(command, tuple_List)
        self.db.commit()

    def insertSession(self, rows):
        '''tuple: (DECK_ID)'''
        command = "INSERT INTO SESSIONS VALUES((SELECT strftime('%s','now')), DECK_ID=?)"
        self.db.execute(command, rows)
        self.db.commit()

    def insertStatistic(self, row):
        '''tuple: (CARD_ID, START_TIME, TIMES_CORRECT, TIMES_ATTEMPTED)'''
        command = "INSERT INTO STATISTICS VALUES(CARD_ID=?, START_TIME=?, TIMES_CORRECT=?, TIMES_ATTEMPTED=?);"
        self.db.execute(command, row)
        self.db.commit()

    def deleteDeck(self, deck_name):
        '''tuple: (deck_name)'''
        t = (deck_name, )
        command = "DELETE FROM STATISTICS WHERE (DECK_ID=?)"
        self.db.execute(command, t)
        command = "DELETE FROM SESSIONS WHERE (DECK_ID=?)"
        self.db.execute(command, t)
        command = "DELETE FROM CARDS WHERE (DECK_ID=?)"
        self.db.execute(command, t)
        command = "DELETE FROM DECKS WHERE (DECK_ID=?)"
        self.db.execute(command, t)
        self.db.commit()

    def getDecks(self):
        command = ("SELECT * FROM DECKS;")
        self.cur.execute(command)
        listOfDecks = self.cur.fetchall()
        return listOfDecks

    def modifyCardData(self, row, deck_name, card_num):
        command = ("UPDATE CARDS SET VOCABULARY=?, DEFINITION=?, PRONUNCIATION=?, IS_STARRED=? "
                   "WHERE DECK_ID= " + deck_name + "AND CARD_ID="+card_num+";")
        self.db.execute(command, row)
        self.db.commit()

    ##################################
    # def dropTable(self,table_name):
    #     command = "DROP TABLE " +"[" + table_name +"]"+ ";"
    #     self.db.execute(command)
    #     self.db.commit()

    # def modifyTableRows(self, table_name, row_data, row_index):
    #     if self.validateRow(row_data, num_rows=7):
    #         print("Table edit: ", row_data, " has been validated.")
    #         print("UPDATING TABLE DATA!", row_data)
    #         print("Updating table at card Num:", row_index)
    #         command = "UPDATE [" + table_name + "] SET STARRED=?, VOCABULARY=?, DEFINITION=?, PRONUNCIATION=?, " \
    #                                                         "CORRECT=?, ATTEMPTED=? WHERE CARDNUM= " + str(row_data.pop(0))
    #         print(command)
    #         self.db.execute(command, row_data)
    #         self.db.commit()
    #         print("Cardnum:", row_data[0], "has been modified.")

    # def addTableRow(self, table_name, row_data):
    #     self.validateRow(row_data)
    #
    #     command = "INSERT INTO " + "[" + table_name + "] " + " (STARRED, VOCABULARY, DEFINITION, PRONUNCIATION," \
    #                                                          " CORRECT, ATTEMPTED) VALUES (?,?,?,?,?,?);"
    #     print(command)
    #     self.db.execute(command, row_data[1:])
    #     self.db.commit()
    #
    # def deleteTableRow(self, table_name, row_index):
    #     command = "DELETE FROM " + "[" + table_name + "]" + " WHERE CARDNUM = " + row_index
    #     self.db.execute(command)
    #     self.db.commit()

    def validateRow(self, row_data, num_rows=7):
        '''This function will check the data types of a list to make sure 1, 5, 6 are integers'''
        # TODO CHANGE LOGIC HERE PROBABLY
        # TODO COME BACK TO CHANGE THE INDEXES OF EACH ROW
        # The row being passed in will include everything including index 0, cardnum (primary key)
        # [CARDNUM ,STARRED, VOCABULARY, DEFINITION, PRONUNCIATION, CORRECT, ATTEMPTED, LASTTIMESTUDIED]

        if len(row_data) != num_rows:
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
        if len(data) == 0:
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
        self.createDeckTable(tablename)

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
        t = (table_name, )
        command = "SELECT CARD_ID, IS_STARRED, VOCABULARY, DEFINITION, PRONUNCIATION FROM CARDS WHERE DECK_ID=?"
        cur = self.db.execute(command, t)
        result = cur.fetchall()
        return result

    def getStarredTableData(self, table_name):
        cur = self.db.execute("SELECT * FROM {}".format("[" + table_name + "] WHERE STARRED = 1"))
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
        pass
        # cur = self.db.execute("SELECT LASTTIMESTUDIED FROM [" + table_name + "];")
        # result = cur.fetchone()
        #
        # try:
        #     result = result[0]
        # except TypeError:
        #     result = '0'
        # print(result)
        # return result

