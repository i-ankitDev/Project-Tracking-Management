import tornado


class BaseHandler(tornado.web.RequestHandler):
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Authorization")

    def options(self, *args, **kwargs):
        """ Handle pre-flight requests (OPTIONS) """
        self.set_status(204) 
        self.finish()