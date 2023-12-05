import sys
from bot.main import main, init


if __name__ == "__main__":
    deploy = "--deploy" in sys.argv or "-d" in sys.argv
    app, msg_handler, PORT, BOT_TOKEN = init(deploy=deploy)
    main(app, msg_handler, PORT, BOT_TOKEN, deploy=deploy)
