from flask import Flask, jsonify, request
import yaml
import boto3
import json

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

pokedex = response['Body'].read().decode('utf-8')

app = Flask(__name__)


@app.route('/api')
def get_all_pokemon():
    all_pokemon = json.loads(pokedex)["pokemon"]

    name = request.args.get("name")

    return_pokemon = None
    if (name):
        for pokemon in all_pokemon:
            if (pokemon["name"].lower() == name):
                return_pokemon = pokemon

    id = request.args.get("id")
    if (id):
        for pokemon in all_pokemon:
            if (pokemon["id"].lower() == id):
                if (return_pokemon and pokemon["name"] != return_pokemon["name"]):
                    return {"message": "No pokemon found"}, 404
                return_pokemon = pokemon

    if (return_pokemon == None):
        return_pokemon = all_pokemon

    return jsonify(return_pokemon)


@app.route('/')
def catch_root():
    return {"message": "Nothing here!"}, 404


@app.route('/<path:path>')
def catch_all(path):
    return {"message": "Nothing here!"}, 404


# The config is only used in development, so only run the dev server if it "exists"
if (config["ACCESS_KEY_ID"] and config["ACCESS_KEY_SECRET"]):
    app.run()
