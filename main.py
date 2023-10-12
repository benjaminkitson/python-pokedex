from flask import Flask, jsonify
import boto3

BUCKET_NAME = "bk-pokedex-bucket"

client = boto3.client('s3')

response = client.get_object(Bucket=BUCKET_NAME, Key='pokedex.json')

pokedex = response['Body'].read().decode('utf-8')

app = Flask(__name__)


@app.route('/')
def get_pokedex():
    return jsonify(pokedex)
