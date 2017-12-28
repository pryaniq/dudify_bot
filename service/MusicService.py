class NotImplemented(Exception):
    def __init__(self):
        super().__init__('This method is not implemented yet')


"""
{name|link|whatever}
    -> resolve
{name}
    -> [service.get(name) for service in services]
{[links_per_service]}
    -> render result
"""


class MusicService():
    # To be overwritten in child classes
    def get(self, entity: str) -> str:
        raise NotImplemented()

    def resolve(self, url: str) -> str:
        raise NotImplemented()

    def recognize(self, url: str) -> bool:
        raise NotImplemented()

    @classmethod
    def is_url(cls, entity):
        # TODO implement here
        raise NotImplemented()
