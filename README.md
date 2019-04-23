# Chicken_Dinner
Still very much in Beta.

This bot keeps track of games won in board games for specific games!
A single win can be added with just `!winner (board game name) @[Discord_user]`
The script automatically parses the board game's name and checks the `game_wins.json` for that game and adds the player to the winners for that game, then adds a win for that player.

If a game is not in the list, it can be added by any user with `!add (board game name)`. For bot setup, you can edit the json directly to add games.

Games known by the bot can be listed with `!list games`.
