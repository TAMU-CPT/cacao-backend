from django.contrib.auth.backends import RemoteUserBackend as RUB


class RemoteUserBackend(RUB):
    create_unknown_user = True
