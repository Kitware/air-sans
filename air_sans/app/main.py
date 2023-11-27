from .core import create_engine
from . import ui


def main(server=None, **kwargs):
    engine = create_engine(server)
    engine.server.controller.on_server_reload = ui.initialize
    ui.initialize(engine.server)
    engine.server.start(**kwargs)


if __name__ == "__main__":
    main()
