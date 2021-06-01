import shlex
from load_data import load_devs, load_games
from get_data import get_data, interpret_command, display_data
from os import path

# create global constants
TABLES = ["game", "developer"]
GAME_FIELDS = ["windows", "linux", "mac", "release", "developer"]
DEVELOPER_FIELDS = ["country", "year", "bestseller"]


# check to see if the database already exists
def data_exists():
    if path.isfile("pc_game_data.db"):
        print("Database already created...Time for Querying!")
        return True
    else:
        return False


# function will load the csv data into the database
def load_data_prompt():
    command = input("> ").lower()
    while command != "load data" and command != "loaddata":
        if command == "help":
            help_user()
        elif command == "quit":
            print("Quitting...")
            quit()
        print("Type 'load data' to prepare database for querying, or 'help' for directions.")
        command = input("> ").lower()
    load_games()
    load_devs()
    print("Loading data... ")


# TODO improve the directions
def help_user():
    print("************ User Guide ************ ")
    print("This tool is designed to access information about PC games and PC game developers.")
    print("To start, you must enter 'load data' to load the database.")
    print("Once data is prepared, you can query in one of three ways: ")
    print("\t1. The Simple Query: Search for a field of a game or developer ")
    print("\t\tby referencing the name of the game or developer (field table name)")
    print("\t\tie. release game Terraria , will return the release date of the game Terraria")
    print("\t2. The Advanced Query: same as simple query but will specify a ")
    print("\t\tcorresponding foreign key in other table (field table1 name1 table2 name2)")
    print("\t\tie. release game Terraria developer Re-Logic , will also return release date of Terraria but if there ")
    print("\t\tare more than one games called Terraria it will find the one made by Re-Logic")
    print("\t3. The Compatibility Query: This allows for you find a list of all PC games that are ")
    print("\t\tcompatible with a certain operating system. It is a two part command, and the second")
    print("\t\tword should always be 'game'. (ie. linux game)")
    print()
    print("Please follow these rules when entering commands: ")
    print("\t1. Put names with multiple words in single or double quotes (ie. bestseller developer 'Gearbox Software'")
    print("\t2. Your commands must have exactly 2, 3 or 5 parts")
    print("\t3. The 2nd word must be 'game' or 'developer'")
    print("\t4. For advanced queries, the 4th word must be the other table option.")
    print("\t\t (if you entered 'game' as 2nd word, 'developer' must be 4th word)")
    print()
    print("The possible fields for the pc games table are windows, linux, mac, release, or developer")
    print("The possible fields for the pc game developers tables are country, year, or bestseller")
    print()


# TODO maybe improve user feedback to give them better hints
def get_command():
    command = input("> ")
    command = command.lower()
    command_list = split_command(command)

    while not is_advanced_query(command_list) and not is_simple_query(command_list) and not command.lower() == "quit":
        if command.lower() == "help":
            help_user()
        else:
            if command.lower() == "load data" or command.lower() == "loaddata":
                print("Database has already been loaded and is ready to query!")
            else:
                print("Invalid command. Type 'help' for more instruction")
        command = input("> ")
        command_list = split_command(command)
    return command_list

# function splits command using shlex
def split_command(command):
    try:
        command_list = shlex.split(command)
    except ValueError:
        print("No closing quotation on substring")
        command_list = []
    return command_list

# function that checks if command is a valid simple query command
def is_simple_query(command_list):
    if len(command_list) == 3:
        table = command_list[1].lower()
        field = command_list[0].lower()
        if table in TABLES:
            if table == TABLES[0]:
                if field in GAME_FIELDS:
                    return True
                else:
                    return False
            else:
                if field in DEVELOPER_FIELDS:
                    return True
                else:
                    return False
        else:
            return False
    # this elif block checks for our special 2 word queries
    elif len(command_list) == 2:
        if command_list[0] in GAME_FIELDS[0:3] and command_list[1] == TABLES[0]:
            return True
        else:
            return False
    else:
        return False

# function checks if command is an advanced query
def is_advanced_query(command_list):
    if len(command_list) == 5:
        first_table = command_list[1].lower()
        second_table = command_list[3].lower()
        field = command_list[0].lower()
        if first_table in TABLES:
            if first_table != second_table and second_table == TABLES[1]:
                if first_table == TABLES[0]:
                    if field in GAME_FIELDS:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


# this function will retrieve query results
def get_query_results(command_list):
    # map command to actual table field names
    new_command_list = interpret_command(command_list)
    return get_data(new_command_list)


def main():
    # give user initial instructions
    #help_user()

    # check if data is loaded, if not then wait for user to type 'load data'
    if not(data_exists()):
        load_data_prompt()

    # get user input
    command_list = get_command()

    # quit if user prompts to
    if command_list[0].lower() == "quit":
        print("Quitting...")
        quit()

    # get results
    results = get_query_results(command_list)

    # display results
    display_data(results, len(command_list))

    # repeat in while loop until user quits
    while True:
        command_list = get_command()
        if command_list[0].lower() == "quit":
            print("Quitting...")
            quit()
        results = get_query_results(command_list)
        display_data(results, len(command_list))


if __name__ == '__main__':
    main()
