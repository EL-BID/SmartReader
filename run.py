 #let try the run seperately
from main import app
if __name__ == '__main__':
    app.run(debug=True, port=8090, host='0.0.0.0', use_reloader=False)
