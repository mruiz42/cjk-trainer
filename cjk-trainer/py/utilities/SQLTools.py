import sqlite3

import sys
class SqlTools():
    def createDatabase(self):
        print("foo")


    def openDatabase(self, dbname):
        #do something
        #print("something")
        #self.db = sqlite3.connect(dbname)
        #check if already open
        self.db = sqlite3.connect(dbname)
        #print(self.db.open(dbname))

        self.cur = self.db.cursor()
        return self.cur

    def closeDatabase(self):
        #print("something")
        self.db.close()

    def insertVocabWordList(self, table_name, headers, vocabword_list):
        header_string = '(' + ','.join(headers + ['ATTEMPTED', 'CORRECT', 'STARRED']) + ')'
        placeholders = '(' + ','.join(['?' for header in headers] + ['0', '0', '0']) + ')'
        command = 'INSERT INTO ' + table_name + header_string + ' VALUES ' + placeholders
        print(command)
        # (null,?,?,?,0,0,0)
        self.db.executemany(command, vocabword_list)
        self.db.commit()


    def createTable(self, table_name):
        #c = self.db.cursor()
        c = self.cur
        # Check if table exists
        # try:
        #     c.execute('SELECT * FROM ' + tablename)
        #     print(c.fetchall())
        #     print("table exists, probably.")
        # except sqlite3.OperationalError:
        #     # Table must not exist
        #     # SEARCH FOR TABLE NAME AND DONT RUN IF FOUND!
        command = ("CREATE TABLE IF NOT EXISTS " + str(table_name) +
                   "(CARDNUM INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "VOCABULARY CHAR,"
                   "DEFINITION CHAR,"
                   "PRONUNCIATION CHAR,"
                   "ATTEMPTED INT,"
                   "CORRECT INT,"
                   "STARRED INT);")

        # Extend table to include
        self.db.execute(command)
        self.db.commit()
        print("table ", table_name, " created!")

    def dropTable(self,table_name):
        command = ""



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
    # def CSVtoSQLFile(self, csvfile, sqlfile, tablename):
    #     '''This function will parse a CSV line where format is as follows:
    #     vocabulary word,pronunciation,definition1;definition2;etc.
    #     (hanzi),(pinyin),(English defn.)
    #     '''
    #     hanzi = ""
    #     pinyin = ""
    #     definition = ""
    #     file = open(csvfile, mode="r")
    #     outfile = open(csvfile + ".sql", mode="w")
    #     outfile.write("CREATE TABLE " + tablename +
    #                   "(\nCARDNUM INT PRIMARY KEY NOT NULL,"
    #                   "\nHANZI CHAR(16),"
    #                   "\nPINYIN CHAR(32),"
    #                   "\nDEFINITION CHAR(64)"
    #                   "\n);\n")
    #     #cardnum = 0
    #     for line in file:
    #         if (len(line) == 0):
    #             print("Empty Line!")
    #         elif (line[0] == '#'):
    #             print("Comment line!")
    #         else:
    #             pos0 = line.find(",")
    #             pos1 = line.find(",", pos0 + 1)
    #             hanzi = line[0:pos0]
    #             pinyin = line[pos0 + 1:pos1]
    #             definition = line[pos1 + 1:-1]
    #             # print(cardnum, " ", hanzi, pinyin, definition)
    #             outfile.write("INSERT INTO " + tablename + " VALUES (" + str(cardnum)
    #                           + ",'" + hanzi + "','" + pinyin + "','" + definition + "');\n")
    #             #cardnum += 1
    #     file.close()
    #     outfile.close()



    # TODO
    #  When I inserted into the table before, I had a typo where it had no comma after PRONUNCIATION in the query,
    #  and it was complaining about 7 values being passed to the command because the hidden cardnum cell was still there
    def CSVtoSQLDatabase(self, csvfile, tablename):
        '''This function will parse a CSV line where format is as follows:
        vocabulary word,pronunciation,definition1;definition2;etc.
        (hanzi),(pinyin),(English defn.)
        '''

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

    if __name__ == "__main__":
        from ..utilities.SQLTools import SqlTools
        sys.path.insert(0, '/home/michael/PycharmProjects/cjk-trainer-master/cjk-trainer')
        tk = SqlTools()
        #tk.CSVtoSQLFile("Vocab", "outputSQL.db", "nihao3")
        tk.openDatabase("test.db")
        #test searching before input
        #tk.findEntry("")
        tk.CSVtoSQLDatabase("/home/michael/PycharmProjects/cjk-trainer-master/cjk-trainer/data/chinese_words/Vocab", "test")
        tup = [(2)]
        tk.cur.execute('SELECT * FROM TEST WHERE CARDNUM = (?)', tup)
        print(tk.cur.fetchone())
        tup = [("发短信")]
        tk.cur.execute("SELECT * FROM TEST WHERE HANZI = (?)", tup)
        print(tk.cur.fetchone())
        tk.closeDatabase()
