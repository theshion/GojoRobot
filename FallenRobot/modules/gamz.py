from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random

# Initialize your Pyrogram bot
from FallenRobot import pbot as app

# Dictionary to store user game states
user_states = {}

# Define the game logic
class Game:
    def __init__(self):
        self.location = "start"
        self.gold = 0
        self.hp = 100
        self.strength = random.randint(1, 10)

# Image URLs for different locations
location_images = {
    "start": "https://example.com/start_image.jpg",
    "forest": "https://example.com/forest_image.jpg",
    "cave": "https://example.com/cave_image.jpg",
    "village": "https://example.com/village_image.jpg",
    "castle": "https://example.com/castle_image.jpg",
}

# Define game locations
locations = {
    "start": {
        "description": "You are at the start. Choose your path.",
        "options": [
            {"text": "Adventure", "next_location": "forest"},
            {"text": "Fight", "next_location": "cave"},
        ],
    },
    "forest": {
        "description": "You venture into the forest.",
        "options": [
            {"text": "Explore", "next_location": "village"},
            {"text": "Return", "next_location": "start"},
        ],
    },
    "cave": {
        "description": "You enter a dark cave.",
        "options": [
            {"text": "Fight the Dragon", "next_location": "castle"},
            {"text": "Retreat", "next_location": "start"},
        ],
    },
    "village": {
        "description": "You arrive at a peaceful village.",
        "options": [
            {"text": "Trade", "next_location": "forest"},
            {"text": "Rest", "next_location": "castle"},
        ],
    },
    "castle": {
        "description": "You approach a grand castle.",
        "options": [
            {"text": "Challenge the King", "next_location": "start"},
            {"text": "Rest", "next_location": "village"},
        ],
    },
}

# Game states
game_states = {}

@app.on_message(filters.command("start"))
def start_game(client, message):
    user_id = message.from_user.id
    game = Game()
    game_states[user_id] = game
    send_location_description(message, game.location)

def send_location_description(message, location):
    user_id = message.from_user.id
    game = game_states.get(user_id)

    if game and location in locations:
        location_data = locations[location]
        keyboard = []
        for option in location_data["options"]:
            keyboard.append([InlineKeyboardButton(option["text"], callback_data=option["text"])])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.reply_photo(location_images[location], location_data["description"], reply_markup=reply_markup)

@app.on_callback_query()
def handle_callback(client, callback_query):
    user_id = callback_query.from_user.id
    game = game_states.get(user_id)

    if game:
        user_choice = callback_query.data
        location_data = locations[game.location]

        if any(option["text"] == user_choice for option in location_data["options"]):
            next_location = [option["next_location"] for option in location_data["options"] if option["text"] == user_choice][0]
            game.location = next_location
            send_location_description(callback_query.message, next_location)
