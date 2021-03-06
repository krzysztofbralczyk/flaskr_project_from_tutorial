import os  # moduł zawierający funkcje związane z systemem
# operacyjnym np. tworzenie stringa - ścieżki, mając tylko nazwy
# folderów i plików. funkcja sama dodaje odpowidnie łączniki zależne od systemu

from flask import Flask  # z modułu framework'a flask importuje klasę Flask która
# jest podstawą aplikacji

def create_app(test_config=None):  # funkcja zwnana fabryką aplikacji, tworzy i
    # zwraca instancje aplikacji, dodatkowo przyjmuje test_config, który domyślnie
    # ma wartość None, a w przypadku podania ścieżki pliku, będzie tworzył aplikacje
    # na bazie zawartości pliku

    app = Flask(__name__, instance_relative_config=True)  # __name__ to nazwa
    # obecnego modułu czyli __init__.py, przekazujemy ten parametr zawsze do
    # aplikacji Flaskowej, instance_relative_config ustawia tzw. instance folder
    # , czyli folder w tym samym folderze co flaskr, w którym przechowywany
    # jest config wyłącznie dla danej instancji. Z reguły nie chcemy go załączać
    # do gita bo może on zawierać wrażliwe informacje jak np. klucze API
    # lub ustawiania zależne od środowiska(np systemu operacyjnego). Dzieki
    # temu ustawianiu pozniej mozemy uzyc
    # app.config.from_pyfile('config.py') i flask automatycznie bedzie szukal
    # config.py w folderze instance\

    from . import db # import from folder containing this module, a module
    # written by me containing functions to be usedwith database like initializing,
    # creating connection and closing connection and init-db command line command

    db.init_app(app) # add function in db module to app instance

    from . import auth
    app.register_blueprint(auth.bp)

    app.config.from_mapping(  # ustawia domyśle ustawienia
        SECRET_KEY='tobechanged',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )  # os.path.join tworzy string'a ze ścieżką składająca się z elementów
    # zawartych w nawiasie. app.instance_path zawiera ścieżkę do aktualnej
    # instancji

    from . import blog  # import blog module
    app.register_blueprint(blog.bp)  # register blueprint with the app
    app.add_url_rule('/', endpoint='index')  # blog blueprint adds URL rule '/' to the endpoint 'blog.index'. But auth
    # blueprint redirects to url_for('index'), where 'index' is non-existing endpoint. This line adds this endpoint,
    # and now we have both index and blog.index endpoints pointing to url '/'. Both url_for('blog.index') and
    # url_for('index') will return '/'

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
        # jestli test_config nie zostal podany(czyli nie testujemy) to
        # wgraj z folderu instance/ modul config.py
    else:
        app.config.from_mapping(test_config)
        # jesli test_config zostął podany, wgraj z niego ustawienia

    try:
        os.makedirs(app.instance_path)
        # instance folder nie jest tworzony domyślnie, więc trzeba go utworzyć
        # jeśli nie istnieje, zwłaszcza że będzie się w nim znajdować
        # baza danych sqlite
        # os.makedirs tworzy wszystkie wymagany foldery według podanej ścieżki
    except OSError:
        # jeśli folder już instnieje to OSError will be raised, co możemy
        # przechwycić i pominąć
        pass

    @app.route('/hello')
    def hello():
        return "Hello from Poland!"

    return app
