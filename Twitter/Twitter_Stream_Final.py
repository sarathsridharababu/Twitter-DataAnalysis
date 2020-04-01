from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pykafka import KafkaClient

API_KEY = '6DS1TKQB21KwjjZLuldZjVV4q'
API_SECRET_KEY = 'wWS7p8HgeS5rSLpamCY0uPtn9ollEWXcP8ax91Q3wpofttSTaz'
ACCESS_TOKEN = '1221858812048572416-TbTXvCqnoSyiFoVmF25Vk40FxdbO4X'
ACCESS_TOKEN_SECRET= '4ysJmarNI3jj5Vmctbx6uxWyqnyfQK2lcI7KYPDKaZKJ7'

client = KafkaClient(hosts="localhost:9092")

topic = client.topics['twitterdata1']
producer = topic.get_sync_producer()


class StdOutListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        super().__init__()
        self.fetched_tweets_filename = fetched_tweets_filename
        self.counter = 0
        self.limit = 2000000

    def on_data(self, data):
        try:
            if self.counter < self.limit:
                self.counter += 1
                print(data)
                with open(self.fetched_tweets_filename, 'a') as tf:
                    tf.write(data)
                producer.produce(data.encode('ascii'))
                return True
            else:
                return False
        except BaseException as e:
            pass

#To check if twitter as issued notice on rate limit, if yes then break the stream

    def on_error(self, status):
        if status == 420:
        	return false
        print(status)


if __name__ == "__main__":
    fetched_tweets_filename = "test_tweets_limits.txt"
    auth = OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    listener = StdOutListener(fetched_tweets_filename)
    stream = Stream(auth, listener)
    stream.filter(track=['#Coronavirus'])


