import api

application = app = api.create_app()

if __name__ == 'main':
    app.run(DEBUG=True)