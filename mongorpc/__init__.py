from pymongo import MongoClient
import inspect
from time import sleep
import logging

class MongoRPCClient(object):
    def __init__(self, mongo_uri="mongodb://localhost:27017/default",
        rpc_collection="rpc", error_collection="rpc_errors"):

        self.collection = rpc_collection
        self.error_collection = error_collection

        if mongo_uri:
            self.db = MongoClient(mongo_uri).get_default_database()
        else:
            self.db = MongoClient().get_default_database()

    def call(self, method, *args, **kwargs):
        request = {
            'method': method,
            'args': args,
            'kwargs': kwargs,
        } # todo add id...
        return self.db[self.collection].insert(request)


    def __getattr__(self, name):
        def wrap(*args, **kwargs):
            return self.call(name, *args, **kwargs)
        return wrap



class MongoRPC(object):
    factory = dict()

    def __init__(self, mongo_uri="mongodb://localhost:27017/default",
        polling_interval=5, rpc_collection="rpc", error_collection="rpc_errors"):

        if mongo_uri:
            self.db = MongoClient(mongo_uri).get_default_database()
        else:
            self.db = MongoClient().get_default_database()

        self.polling_interval = polling_interval
        self.collection = rpc_collection
        self.error_collection = error_collection

    def register_callback(self, f, name=""):
        if len(name) > 0:
            self.factory[name] = f
        else:
            self.factory[f.__name__] = f

    def register(self, name=""):
        def decorator(f):
            self.register_callback(f, name=name)
            return f
        return decorator


    def call(self, method, args, kwargs):
        f = self.factory[method]
        converted = dict()
        defined_args,_,_,_ = inspect.getargspec(f) # signature(f).parameters.keys()
        for arg in defined_args:
            if arg in kwargs:
                converted[arg] = kwargs[arg]
        return self.factory[method](*args, **converted)

    def report_failure(self, item, error):
        item["error"] = str(error)
        self.db[self.error_collection].insert(item)

    def poll(self):
        item = self.db[self.collection].find_one({})
        self.db[self.collection].remove(item)
        return item

    def start(self):
        self.run()

    def run(self):
        while True:
            item = self.poll()
            try:
                if item:
                    logging.info("RPC-Call {}".format(item["method"]))
                    self.call(item["method"], item["args"], item["kwargs"])
                    continue
            except Exception as err:
                logging.error(err)
                self.report_failure(item, err)
            sleep(self.polling_interval)

    def remove_all_requests(self):
        self.db[self.collection].remove({})

class ScheduledMongoRPC(MongoRPC):
    def poll(self):
        return self.db[self.collection].find_one_and_delete({ '_execute_at':
            { '$lt': datetime.now() } })
