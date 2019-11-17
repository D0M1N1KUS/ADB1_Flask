from db import DbContainer

app = DbContainer.get_app()

if __name__ == '__main__':
    # app = Flask(__name__, instance_relative_config=True)
    app.run(debug=True)


