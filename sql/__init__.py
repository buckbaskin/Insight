'''
sql - Smart Queueing Library

Queue all the queue stuff that I'd like to do.
'''
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
