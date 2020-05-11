from rest_framework.routers import DefaultRouter


class OptionalSlashDefaultRouter(DefaultRouter):
    def __init__(self):
        super(DefaultRouter, self).__init__()
        self.trailing_slash = '/?'
