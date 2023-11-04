#by t.me/fatherOFpaul
import random
from pyrogram import Client, filters
from FallenRobot import pbot as app

# Define the game state
game_states = {}
@app.on_message(filters.command("gplay", prefixes="/"))
async def start_game(client, message):
    user_id = message.from_user.id

    if user_id not in game_states:
        game_states[user_id] = {
            "current_location": "beach",
            "inventory": [],
            "score": 0,
        }
        await message.reply("Welcome to the Mystery Island Adventure game! You find yourself on a mysterious island. Explore and uncover its secrets.")

@app.on_message(filters.command("explore", prefixes="/"))
async def explore_location(client, message):
    user_id = message.from_user.id
    if user_id in game_states:
        current_location = game_states[user_id]["current_location"]
        
        if current_location == "beach":
            game_states[user_id]["score"] += 10
            game_states[user_id]["inventory"].append("Seashell")
            game_states[user_id]["current_location"] = "jungle"
            await message.reply("You explore the beach and find a seashell. You continue into the dense jungle.")
        elif current_location == "jungle":
            game_states[user_id]["score"] += 15
            game_states[user_id]["current_location"] = "cave"
            await message.reply("As you journey through the jungle, you discover an entrance to a mysterious cave. You enter the cave.")
        elif current_location == "cave":
            game_states[user_id]["score"] += 20
            game_states[user_id]["current_location"] = "treasure"
            await message.reply("Inside the cave, you find a hidden treasure chest! You open it and uncover valuable treasures.")

@app.on_message(filters.command("inventory", prefixes="/"))
async def check_inventory(client, message):
    user_id = message.from_user.id
    if user_id in game_states:
        inventory = game_states[user_id]["inventory"]
        await message.reply(f"Your inventory contains: {', '.join(inventory)}")

@app.on_message(filters.command("score", prefixes="/"))
async def check_score(client, message):
    user_id = message.from_user.id
    if user_id in game_states:
        score = game_states[user_id]["score"]
        await message.reply(f"Your current score is: {score}")

@app.on_message(filters.command("reset", prefixes="/"))
async def reset_game(client, message):
    user_id = message.from_user.id
    if user_id in game_states:
        del game_states[user_id]
        await message.reply("Game progress reset. You can start a new adventure anytime.")
