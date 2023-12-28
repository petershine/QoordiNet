

def main():
    from . import app_constants
    from .qoordinet_app import QoordiNetAppManager
    appManager = QoordiNetAppManager(app_constants.APP_NAME, app_constants.LOG_FILE_PATH)

    from . import interfaces
    interfaces.webAppManager = appManager

    import uvicorn
    config = uvicorn.Config(f"{interfaces.__name__}:app", host="0.0.0.0", port=app_constants.PORT_NUMBER, log_config=None)
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()
