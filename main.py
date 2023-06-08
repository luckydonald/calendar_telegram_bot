from brony_meetup_bot.main import start
from luckydonaldUtils.logger import logging


if __name__ == '__main__':
    logging.add_colored_handler('root', level=logging.DEBUG)
    start()
# end def
