from zero import ZeroServer


async def write_to_db() -> str:
    pass


async def read_from_db() -> list[str]:
    pass

if __name__ == "__main__":
    app = ZeroServer(port=8888)
    app.register_rpc(write_to_db)
    app.register_rpc(read_from_db)
    app.run()
