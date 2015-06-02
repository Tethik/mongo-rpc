from unittest import TestCase
from mongorpc import MongoRPC, MongoRPCClient

class TestRPC(TestCase):

    def setUp(self):
        self.mongo_uri="mongodb://localhost:27017/testrpc"
        self.rpc = MongoRPC(self.mongo_uri)
        self.rpc.remove_all_requests()


    def test_register_with_name(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register("woot")
        def method():
            return "test"

        client = MongoRPCClient(self.mongo_uri)
        print(client.call("woot"))
        self.assertEqual(rpc.call(**rpc.poll()), "test")
        print(client.woot())
        self.assertEqual(rpc.call(**rpc.poll()), "test")


    def test_register_and_call(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def method():
            return "test"

        client = MongoRPCClient(self.mongo_uri)
        print(client.call("method"))

        self.assertEqual(rpc.call(**rpc.poll()), "test")

    def test_call_with_attribute(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def hello():
            return "world"

        client = MongoRPCClient(self.mongo_uri)
        print(client.hello())

        self.assertEqual(rpc.call(**rpc.poll()), "world")

    def test_call_with_named_arg(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def hello(msg):
            return msg

        client = MongoRPCClient(self.mongo_uri)
        print(client.hello(msg="world"))

        self.assertEqual(rpc.call(**rpc.poll()), "world")


    def test_call_with_arg_list(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def hello(msg, wat):
            return msg, wat

        client = MongoRPCClient(self.mongo_uri)
        print(client.hello(123, "world"))

        self.assertEqual(rpc.call(**rpc.poll()), (123, "world"))

    def test_call_with_mixed_args(self):
        rpc = MongoRPC(self.mongo_uri)

        @rpc.register()
        def hello(host, msg, wat=None):
            return host, msg, wat

        client = MongoRPCClient(self.mongo_uri)
        print(client.hello(123, "world", wat=1.0))

        self.assertEqual(rpc.call(**rpc.poll()), (123, "world", 1.0))

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
