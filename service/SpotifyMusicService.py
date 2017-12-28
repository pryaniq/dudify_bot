from service.MusicService import MusicService


class SpotifyMusicService(MusicService):
    def recognize(self, url: str) -> bool:
        if 'spotify' in url.lower():
            return True

    def resolve(self, url: str) -> str:
        return 'songname'

    def get(self, entity: str) -> str:
        return 'songurl'

    