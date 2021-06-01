import sqlite3


# receives list of commands and translates to language consistent with the table
def interpret_command(commands):
    input_to_db_dict = {
        "game": "games",
        "developer": "dev",
        "windows": "is_windows_compatible",
        "mac": "is_mac_compatible",
        "linux": "is_linux_compatible",
        "release": "steam_release_date",
        "country": "country",
        "year": "year_established",
        "bestseller": "best_selling_game_fk"
    }

    # will store commands mapped to corresponding database field and table names
    new_commands = []

    # convert from user input to language consistent with database
    for command in commands:
        if command in input_to_db_dict:
            new_commands.append(input_to_db_dict[command])
        else:
            new_commands.append(command)
    # remap game_developer field
    if new_commands[0] == "dev":
        new_commands[0] = "game_developer_fk"

    return new_commands


# builds command for simple query
def simple_command_builder(target, table, field, value):
    command = "SELECT "
    command += target
    if table == "games":
        command += ", game_developer_fk"
    command += " FROM "
    command += table
    command += " WHERE "
    command += field
    command += " = \""
    command += value
    command += "\""
    return command


# builds command for advanced query
def advanced_command_builder(target, table_1, table_2, join_field_1, join_field_2, field_1, field_2, value_1, value_2):
    command = "SELECT "
    command += target
    command += " FROM "
    command += table_1
    command += " INNER JOIN "
    command += table_2
    command += " ON "
    command += table_1
    command += "."
    command += join_field_1
    command += "="
    command += table_2
    command += "."
    command += join_field_2
    command += " WHERE "
    command += field_1
    command += "= \""
    command += value_1
    command += "\" AND "
    command += field_2
    command += " = \""
    command += value_2
    command += "\""
    return command


# get the data
def get_data(command_array):
    conn = sqlite3.connect("pc_game_data.db")
    c = conn.cursor()
    # OS Simple query
    if len(command_array) == 2:
        command = simple_command_builder("game_title", "games", command_array[0], "yes")
    # Simple query
    elif len(command_array) == 3:
        field = ""
        if command_array[1] == "games":
            field = "game_title"
        elif command_array[1] == "dev":
            field = "game_developer"
        command = simple_command_builder(command_array[0], command_array[1], field, command_array[2])
    # Advanced query
    elif len(command_array) == 5:
        join_field_1 = "game_developer_fk"
        join_field_2 = "pk"
        field_1 = "game_title"
        field_2 = "game_developer"

        command = advanced_command_builder(command_array[0], command_array[1], command_array[3], join_field_1,
                                           join_field_2, field_1, field_2, command_array[2], command_array[4])
    # Invalid query
    else:
        return -1

    try:
        c.execute(command)

        results = c.fetchall()
        if results is None:
            results = []
        # if the results are a foreign key, we can't leave it as an integer
        # we need to convert it to the title of the game or name of the developer
        # this requires another SELECT statement
        if len(results) != 0:
            if command_array[0] == "game_developer_fk" or command_array[0] == "best_selling_game_fk":
                foreign_results = []
                if command_array[0] == "game_developer_fk":
                    for result in results:
                        pk = result[0]
                        foreign_command = "SELECT game_developer FROM dev WHERE pk = '" + pk + "'"
                        c.execute(foreign_command)
                        foreign_result = c.fetchall()
                        foreign_results.append(foreign_result[0])
                else:
                    for result in results:
                        pk = result[0]
                        foreign_command = "SELECT game_title FROM games WHERE pk = '" + pk + "'"
                        c.execute(foreign_command)
                        foreign_result = c.fetchall()
                        foreign_results.append(foreign_result)
                return [foreign_results, []]
            else:
                # if a games query has multiple results, we must indicate the developer of the game
                if len(results) > 1 and command_array[1] == "games":
                    developer_list = []
                    for result in results:
                        pk = result[1]
                        developer_command = "SELECT game_developer FROM dev WHERE pk = '" + pk + "'"
                        c.execute(developer_command)
                        developer_result = c.fetchall()
                        developer_list.append(developer_result[0])
                    return [results, developer_list]
                else:
                    return [results, []]
        else:
            return [results, []]

    except BaseException as be:
        print(be)


# display data in a user friendly way
def display_data(results, command_length):
    print("Your search found the following results: \t")
    if len(results[0]) == 0:
        print("Sorry, no results found.")
    elif len(results[1]) != 0:
        i = 0
        for result in results[0]:
            if command_length == 2:
                print(result[0].capitalize() + " by " + results[1][i][0].capitalize())
            else:
                print(results[1][i][0].capitalize() + "'s version: " + result[0].capitalize())
            i += 1
    else:
        for result in results[0]:
            print(result[0])


