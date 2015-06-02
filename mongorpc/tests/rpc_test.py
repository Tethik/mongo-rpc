from unittest import TestCase
from mongorpc import MongoRPC, MongoRPCClient

class TestRPC(TestCase):

    def setUp(self):
        self.mongo_uri="mongodb://localhost:27017/testrpc"
        self.rpc = MongoRPC(self.mongo_uri)
        self.rpc.remove_all_requests()

    def poll_and_call(self, rpc):
        item = rpc.poll()
        print(item)
        return rpc.call(item["method"], item["args"], item["kwargs"])

    def test_register_with_name(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register("woot")
        def method():
            return "test"

        client = MongoRPCClient(self.mongo_uri)
        print(client.call("woot"))

        self.assertEqual(self.poll_and_call(rpc), "test")
        print(client.woot())
        self.assertEqual(self.poll_and_call(rpc), "test")


    def test_register_and_call(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def method():
            return "test"

        client = MongoRPCClient(self.mongo_uri)
        print(client.call("method"))

        self.assertEqual(self.poll_and_call(rpc), "test")

    def test_call_with_attribute(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def hello():
            return "world"

        client = MongoRPCClient(self.mongo_uri)
        print(client.hello())

        self.assertEqual(self.poll_and_call(rpc), "world")

    def test_call_with_named_arg(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def hello(msg):
            return msg

        client = MongoRPCClient(self.mongo_uri)
        print(client.hello(msg="world"))

        self.assertEqual(self.poll_and_call(rpc), "world")


    def test_call_with_arg_list(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def hello(msg, wat):
            return msg, wat

        client = MongoRPCClient(self.mongo_uri)
        print(client.hello(123, "world"))

        self.assertEqual(self.poll_and_call(rpc), (123, "world"))

    def test_call_with_mixed_args(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def hello(host, msg, wat=None):
            return host, msg, wat

        client = MongoRPCClient(self.mongo_uri)
        print(client.hello(123, "world", wat=1.0))

        self.assertEqual(self.poll_and_call(rpc), (123, "world", 1.0))

    # def test_error(self):
    #     rpc = MongoRPC()
    #
    #     @rpc.register()
    #     def method():
    #         return 1 / 0
    #
    #     client = MongoRPCClient()
    #     print(client.call("method"))
    #
    #     self.assertEqual(rpc.call(**rpc.poll()), "test")
