# mongo-rpc
Experimental python RPC using a mongodb collection

# Usage:

Server
```
from mongorpc import MongoRPC

rpc = MongoRPC()

@rpc.register()
def hello(msg):
  print("hello {}".format(msg))

rpc.start()
```

Client
```
from mongorpc import MongoRPCClient

client = MongoRPCClient()
client.hello("world")
```

# Future work
* Perhaps Conform to [jsonrpc standard](http://www.jsonrpc.org/specification).
* Asynchronous versus synchronous calls?
* Save results from method call.
* Transaction safety, to support more than one executing server?
* Perhaps serialize method code. Eggify?
* Tailable/capped collections.
