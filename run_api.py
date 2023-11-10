from api import create_api_app

app = create_api_app()

if __name__ == '__main__':
    app.run(port=8081, debug=True)