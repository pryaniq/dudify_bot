from config import token

from telebot import types
from telebot import TeleBot

from service.MusicService import MusicService
from service.SpotifyMusicService import SpotifyMusicService


class DudifyBot(TeleBot):
    # Token here is used from outer scope (from config)
    def __init__(self, token=token, threaded=True, skip_pending=False, num_threads=2):
        super().__init__(token, threaded, skip_pending, num_threads)
        self.services = [SpotifyMusicService()]

    def search(self, message):
        # TODO Here should be validation for lazy query search (inline usage)
        # Take here song name
        entity = message.text
        if MusicService.is_url(entity):
            # Resolve song by its url using its service
            # Google `list comprehension`
            resolved = [service.resolve(entity) for service in self.services if service.recognize(entity)]
            # ensure we have only one resolved song name, otherwise fix that in recognize method
            assert len(resolved) == 1
            entity = resolved.pop()
        # Here we know that it's a song name
        song_name = entity
        # Generate links using services' clients implementations
        # TODO should we take care of getting link from the same service if link provided?
        # - filter out this service
        # - get link and compare with provided one (and what?)
        # - get link and ignore old one
        links = [service.get(song_name) for service in self.services]
        return self.format_response(links)

    def format_response(self, text, *args):
        # Perhaps we cannot just return list of links, so
        # TODO add pretty formatting here
        return text

    @bot.message_handler(content_types=["text"])
    def repeat_all_messages(self, message):
        # Code is left here just for example
        self.send_message(message.chat.id, self.search(message))

    @bot.inline_handler(func=lambda query: len(query.query) > 0)
    def empty_query(self, query):
        # I suppose here should be 2 different cases:
        # 1) if link given, just show available results
        # 2) if song name is typing - wait until user finishes?
        # Code is left here just for example
        hint = "Введите имя исполнителя или ссылку на него в любом музыкальном сервисе"
        try:
            r = types.InlineQueryResultArticle(
                id='1',
                # parse_mode='Markdown',
                title="Музыкальный бот",
                description=hint,
                input_message_content=types.InputTextMessageContent(
                message_text=self.search(query))
            )
            self.answer_inline_query(query.id, [r])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    bot = DudifyBot()
    bot.polling(none_stop=True)
