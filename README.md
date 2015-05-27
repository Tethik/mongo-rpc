# mongo-rpc
Experimental python RPC using a mongodb collection

# Usage:

Server
```
from mongorpc import MongoRPC

rpc = MongoRPC()

@rpc.register()
def hello():
  print("hello world")

rpc.start()
```

Client
```
from mongorpc import MongoRPCClient

client = MongoRPCClient()
client.hello()
```

# Future work
* Conform to jsonrpc standard.
* Save results from method call.
* Transaction safety, to support more than one executing server?
* Perhaps serialize method code. Eggify?
* Tailable/capped collections.
