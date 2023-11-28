from .core import AirSans


def main(server=None, **kwargs):
    app = AirSans(server)
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
