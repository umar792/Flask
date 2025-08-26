from app import create_app
import os



app = create_app()
if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 5000))
        app.run(debug=True, port=port)
    except Exception as e:
        print(f"Error starting the server: {e}")