import os # moduł zawierający funkcje związane z systemem
# operacyjnym np. tworzenie stringa - ścieżki, mając tylko nazwy
# folderów i plików. funkcja sama dodaje odpowidnie łączniki zależne od systemu

from flask import Flask #z modułu framework'a flask importuje klasę Flask która
# jest podstawą aplikacji

def create_app(test_config=None): #funkcja zwnana fabryką aplikacji, tworzy i
#zwraca instancje aplikacji, dodatkowo przyjmuje test_config, który domyślnie
#ma wartość None, a w przypadku podania ścieżki pliku, będzie tworzył aplikacje
#na bazie zawartości pliku
