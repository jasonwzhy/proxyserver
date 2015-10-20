from twisted.web import server, resource, http
from twisted.internet import reactor, endpoints

class Counter(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader("content-type", "text/plain")
        print "request from :",request.getClientIP()
        print "urlpath:",request.URLPath
        return "I am request #" + str(self.numberRequests) + "\n"

endpoints.serverFromString(reactor, "tcp:888").listen(server.Site(Counter()))
reactor.run()