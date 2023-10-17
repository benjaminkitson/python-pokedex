from flask import Flask, jsonify, request
import yaml
import boto3
import json
from pokedex import Pokedex, Pokemon
from typing import List
from flask_cors import cross_origin

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

app = Flask(__name__)


@app.route('/api')
@cross_origin()
def get_all_pokemon():

    pokedex = Pokedex(json.loads(pokemons)["pokemon"])

    p_id_filter = request.args.get("id")
    if (p_id_filter):
        filtered_pokemons = pokedex.apply_filter("id", p_id_filter)

    name_filter = request.args.get("name")
    if (name_filter):
        filtered_pokemons = pokedex.apply_filter("name", name_filter)

    filtered_pokemons = pokedex.get_filtered_pokemon()

    if (len(filtered_pokemons) == 0):
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
