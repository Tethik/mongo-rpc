from mongorpc import MongoRPC
import logging

logging.basicConfig(level=logging.INFO)
rpc = MongoRPC()

@rpc.register()
def hello(msg):
  print("hello {}".format(msg))

rpc.start()
