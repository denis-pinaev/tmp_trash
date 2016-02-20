class ChangeCacheMiddleware(object):

    kwargs = []
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        self.kwargs=view_kwargs

    def process_response(self, request, response):
        if "document_root" not in self.kwargs:
            response['Pragma'] = 'no-cache'
            response['Cache-Control'] = 'no-cache must-revalidate proxy-revalidate'
        return response