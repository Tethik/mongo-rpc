from mongorpc import MongoRPC

rpc = MongoRPC()

@rpc.register()
def hello():
  print("hello {}".format(msg))

rpc.start()
