import climmob.plugins.utilities as u


class MyPublicView(u.publicView):
    def process_view(self):
        return {"status": 200, "message": "ok"}


class MyPrivateView(u.privateView):
    def __init__(self, request):
        u.privateView.__init__(self, request)
        self.checkCrossPost = False

    def processView(self):

        return {"activeUser": self.user, "message": "Hello word"}
