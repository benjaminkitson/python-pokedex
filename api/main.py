from flask import Flask, jsonify, request
import yaml
import boto3
import json
from api.pokedex import Pokedex, Pokemon
from typing import List

try:
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    config = {
        "ACCESS_KEY_ID": None,
        "ACCESS_KEY_SECRET": None
    }


client = boto3.client(
    's3', aws_access_key_id=config["ACCESS_KEY_ID"], aws_secret_access_key=config["ACCESS_KEY_SECRET"])


response = client.get_object(Bucket="bk-pokedex-bucket", Key='pokedex.json')

pokemons: List[Pokemon] = response['Body'].read().decode('utf-8')
pokedex = Pokedex(json.loads(pokemons)["pokemon"])

app = Flask(__name__)


@app.route('/api')
def get_all_pokemon():

    filtered_pokemons = pokedex.pokemons

    p_id_filter = request.args.get("id")
    if (p_id_filter):
        filtered_pokemons = Pokedex.find_pokemon_by_id(
            filtered_pokemons, p_id_filter)

    name_filter = request.args.get("name")

    if (name_filter):
        filtered_pokemons = Pokedex.find_pokemon_by_name(
            filtered_pokemons, name_filter)

    if (filtered_pokemons == None):
        return {"message": "No matching pokemon found"}, 404

    return jsonify(filtered_pokemons)


@app.route('/')
def catch_root():
    return {"message": "Nothing here!"}, 404


@app.route('/<path:path>')
def catch_all(path):
    return {"message": "Nothing here!"}, 404


# The config is only used in development, so only run the dev server if it "exists"
if (config["ACCESS_KEY_ID"] and config["ACCESS_KEY_SECRET"]):
    app.run()
