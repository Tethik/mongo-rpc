from mongorpc import MongoRPC

rpc = MongoRPC()

@rpc.register()
def hello(msg):
  print("hello {}".format(msg))

rpc.start()
