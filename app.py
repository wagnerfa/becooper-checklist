from config import create_app

app = create_app()

if __name__ == "__main__":
    # In development, enable debug and reloader
    app.run(host='0.0.0.0', port=5000, debug=True)
