import tweepy
import pandas as pd
from google.cloud import storage
import os
import json

# Cargar el archivo JSON
with open("config.json", "r") as file:
    config = json.load(file)

# Obtener el token
BEARER_TOKEN = config.get("BEARER_TOKEN")



# Configurar autenticación de Twitter
# bearer_token = 'TU_BEARER_TOKEN'
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Definir consulta y parámetros
query = '8M -is:retweet lang:es'

# Guardar DataFrame en un archivo CSV
csv_filename = 'tweets.csv'

numberTweets = 50

tweets = client.search_recent_tweets(query=query, tweet_fields=['author_id', 'created_at'], max_results=numberTweets)

# Procesar datos y almacenarlos en un DataFrame
data = []
for tweet in tweets.data:
    data.append([tweet.id, tweet.author_id, tweet.created_at, tweet.text])
df = pd.DataFrame(data, columns=['id', 'author_id', 'created_at', 'text'])


# Verificar si el archivo ya existe para manejar el encabezado
file_exists = os.path.isfile(csv_filename)

df.to_csv(csv_filename, mode='a', header=not file_exists, index=False, encoding='utf-8')

