from unittest import TestCase
from mongorpc import MongoRPC, MongoRPCClient

class TestRPC(TestCase):

    def test_register_with_name(self):
        rpc = MongoRPC()

        @rpc.register("woot")
        def method():
            return "test"

        client = MongoRPCClient()
        print(client.call("woot"))

        self.assertEqual(rpc.call(**rpc.poll()), "test")


    def test_register_and_call(self):
        rpc = MongoRPC()

        @rpc.register()
        def method():
            return "test"

        client = MongoRPCClient()
        print(client.call("method"))

        self.assertEqual(rpc.call(**rpc.poll()), "test")
