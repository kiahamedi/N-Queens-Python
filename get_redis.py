import redis

r = redis.Redis(host='127.0.0.1', port = 6379, db=0)

fitness = r.keys()

for fitnes in fitness:
    print("%s:%s" % (r.get(fitnes), fitnes))
