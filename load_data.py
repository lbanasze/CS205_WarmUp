import sqlite3


# load developer table
def load_devs():
    try:
        # connect
        con = sqlite3.connect("pc_game_data.db")
        c = con.cursor()

        # create table
        c.execute('''CREATE TABLE dev (pk,game_developer,country,year_established,best_selling_game_fk)''')

        # read in from csv
        with open('game_developers_data.csv', 'r') as f:
            # eats the header
            f.readline()

            # get rest of lines
            lines = f.readlines()

            # iterate through lines
            for line in lines:
                # convert to lowercase
                line = line.lower()

                # eat newline and split into array by commas
                line = line.rstrip()
                line = line.lower()
                data_array = line.split(",")

                # Insert values
                c.execute("INSERT INTO dev (pk, game_developer, country, year_established, best_selling_game_fk) VALUES"
                      " (?, ?, ?, ?, ?)", data_array)

        con.commit()
        return True
    except BaseException as be:
        print(be)
        return False
    finally:
        if c is not None:
            c.close()
        if con is not None:
            con.close()


# create games table
def load_games():
    try:
        # connect
        con = sqlite3.connect("pc_game_data.db")
        c = con.cursor()

        # create table
        c.execute('''CREATE TABLE games (pk,game_title,is_windows_compatible,is_mac_compatible, is_linux_compatible, 
        steam_release_date, game_developer_fk)''')

        # read from csv
        with open('games_data.csv', 'r') as f:
            f.readline()
            lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                line = line.lower()
                data_array = line.split(",")
                c.execute("INSERT INTO games (pk, game_title, is_windows_compatible, is_mac_compatible, "
                          "is_linux_compatible, steam_release_date, game_developer_fk) VALUES"
                          " (?, ?, ?, ?, ?, ?, ?)", data_array)

        con.commit()
        return True
    except BaseException as be:
        print(be)
        return False
    finally:
        if c is not None:
            c.close()
        if con is not None:
            con.close()

