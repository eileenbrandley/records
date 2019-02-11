from records import app
import os
import sys

app_path = os.path.dirname(os.path.realpath(__file__)) + '/../python/'
sys.path.append(app_path)

if __name__ == "__main__":
    app.run()