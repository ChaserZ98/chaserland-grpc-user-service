from chaserland_grpc_user_service.bootstrap.app import create_server

server = create_server()


def main():
    server.run()


if __name__ == "__main__":
    main()
