from chaserland_grpc_user_service.bootstrap.app import create_server

server = create_server()

if __name__ == "__main__":
    server.run()
