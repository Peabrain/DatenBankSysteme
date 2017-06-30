# Übung 7
# Andreas Timmermann, Alena Dudarenok

from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from bs4 import BeautifulSoup
import json
import pandas as pd
import psycopg2
import requests
from email.utils import parsedate
import csv


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        data_tmp = json.loads(data);
        tw_timestamp = data_tmp["created_at"]
        tw_text = data_tmp["text"]
        user = data_tmp["user"]
        tw_user = user["screen_name"]
#        tweets['text'] = map(lambda tweet: tweet['text'], data)
        print(tw_timestamp,tw_user,tw_text)
        #csv_writer.writerow({'created': tw_timestamp, 'user': tw_user, 'text': tw_text.replace('\\u','')})
        return True

    def on_error(self, status):
        print(status)


# this function returns a soup page object
def getPage(url):
    r = requests.get(url)
    data = r.text
    spobj = BeautifulSoup(data, "lxml")
    return spobj


def connect():

    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="dbs", user="postgres", password="postgres")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def main():

    consumer_key        = "t3l8llVayMUCRLwh217fUY1p3"
    consumer_secret     = "JwqWePyGZuUJzXaGId7jv2iPe3EmLhkFoIbWBDGTf3W0I89lef"
    access_token        = "849205479331033088-WdPOGAMZ7dPLuP7WnpejEN62wEsVzQn"
    access_token_secret = "e3FXvPQeWlmmBQ5ylxTzuCZS6WdpVNLKeG1MYsLwMKpMa"

    ofile  = open('ttest.csv', "w")
    fieldnames = ['created', 'user','text']
    global csv_writer
    csv_writer = csv.DictWriter(ofile, fieldnames=fieldnames)
    csv_writer.writeheader()


    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=['@realDonaldTrump'])

    ofile.close()

if __name__ == '__main__':
    main()
