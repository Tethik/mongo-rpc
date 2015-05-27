from mongorpc import MongoRPC

rpc = MongoRPC()

@rpc.register()
def hello():
  print("hello world")

rpc.start()
