# Created by Ada
# Keep track of how many times each person has won games listed in 'winner_list.json'
#!TODO: Add more options to "list" command

import json, discord
from discord.ext.commands import Bot

# Update game wins. Saves data to file, then revamps its own data
def update_data(winner_list_local={}):
    # If we already have data, save it. Then grab it and return winner_list
    # Automatically imports as a dictionary
    if winner_list_local:
        with open("game_wins.json", 'w', encoding='utf-8') as win_data:
            json.dump(win_data)
    with open("game_wins.json", 'r', encoding='utf-8') as win_data:
        winner_list_local = json.load(win_data)
    return winner_list_local

#====================================================
#====================================================
# Define bot. All bot commands begin with "!"
win_bot = Bot(command_prefix = "!")
# When bot connects, prints logging info to stdout and announces herself in chat
@win_bot.event
async def on_ready():
    print('Winner_Bot has Logged On')
    print('Name: {}'.format(win_bot.user.name))
    print('ID: {}'.format(win_bot.user.id))
    return await win_bot.say("Chicken Dinner is online!")

# Add a game to The List
@win_bot.command(name='add', pass_context=True, hidden=True)
async def add_game(ctx):
    message = str(ctx.message.content).strip()
    _bg, *game_name = message.split(' ')
    game_name = ' '.join(game_name).title()
    winner_list[game_name] = {}
    winner_list = update_data(winner_list)
    return await win_bot.say(f"{game_name} has been added to the game list!")


# List all the games or winners of games
#!TODO: Very incomplete. Not much more to say
@win_bot.command(name='list', pass_context=True, hidden=True)
async def list_games(ctx):
    message = str(ctx.message.content).strip()
    _bg, option, *game_name = message.split(' ')
    game_name = ' '.join(game_name).title()

    #!TODO: Add the following:
    #  "list [game_name]" for win counts for [game_name]
    #  ...possibly need to nest another dictionary inside this one. Not sure yet
    options = {
        "games": 'I know the following games:\n'+'\n'.join(winner_list.keys())
        }
    list_response = options[option]
    return await win_bot.say(list_response)


# "!winner game name @[player_id]"
@win_bot.command(name='winner', pass_context=True, hidden=True)
async def add_win(ctx):
    # Grab message content, strip away any extra whitespace
    message = str(ctx.message.content).strip()
    # Most game names will be split up, so we'll catch all of them in *game_name then join them again with spaces
    _bg, *game_name, player_id = message.split(' ')
    game_name = ' '.join(game_name)

    # Verify that game exists. If not, prompt them to add it
    if game_name.title() not in winner_list.keys():
        return await win_bot.say(f"I don't know the game \"{game_name}\"...\nTry adding it with `!add {game_name}`. Or I can print out all the games I know with `!list games`")

    # Verify that player exists for that game. If not, add them with 0 wins
    # All player_ids will/should be in form of "<@xxxxxxxx>"
    if player_id.startswith("<@"):
        if player_id not in winner_list[game_name]:
            winner_list[game_name][player_id] = 0
    else:
        return await win_bot.say("Can't find the player '{player_id}'. Make sure you @ them.")

    # Update win counts in the dictionary, then dump data to file
    winner_list[game_name][player_id] += 1
    winner_list = update_data(winner_list)

    return await win_bot.say(f"{player_id} has won {game_name}!")

#====================================================
#====================================================
def main():
    winner_list = update_data()
    # Get your own token, nerd
    win_bot.run(token)

if __name__ == "__main__":
    main()
