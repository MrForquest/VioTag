from all_resources import *
from requests import get


def api_test_local():
    # Получение поста по id
    print(get(' http://127.0.0.1:5000/api/v1/post/1').json())
    print()
    # Исключение
    print(get(' http://127.0.0.1:5000/api/v1/post/0').json())
    print()
    # Получение всех постов
    print(get(' http://127.0.0.1:5000/api/v1/posts').json())
    print()
    # Получение комментариев к посту по id
    print(get(' http://127.0.0.1:5000/api/v1/comments_post/1').json())
    print()
    # Исключение
    print(get(' http://127.0.0.1:5000/api/v1/comments_post/1000000000').json())
    print()
    # Получение комментария по id
    print(get(' http://127.0.0.1:5000/api/v1/comment/1').json())
    print()
    # Исключение
    print(get(' http://127.0.0.1:5000/api/v1/comment/1000000000').json())
    print()
    # Получение постов по id тэга
    print(get(' http://127.0.0.1:5000/api/v1/tag/1').json())
    print()
    # Исключение
    print(get(' http://127.0.0.1:5000/api/v1/tag/1000000000').json())
    print()


def api_test_remote_server():
    address = ["http://viotag.ru/api/v1/post/1", "http://viotag.ru/api/v1/post/0",
               "http://viotag.ru/api/v1/posts", "http://viotag.ru/api/v1/comments_post/1",
               "http://viotag.ru/api/v1/comments_post/1000000000",
               "http://viotag.ru/api/v1/comment/1",
               "http://viotag.ru/api/v1/comment/1000000000", "http://viotag.ru/api/v1/tag/1",
               "http://viotag.ru/api/v1/tag/1000000000"]
    if get(address[0]):
        print(get(address[0]))
    else:
        print("ошибка с получением поста по id")

    if get(address[1]):
        print(get(address[1]))
    else:
        print("плановая ошибка")

    if get(address[2]):
        print(get(address[2]))
    else:
        print("ошибка с получением всех постов")

    if get(address[3]):
        print(get(address[3]))
    else:
        print("ошибка с получением комментариев к посту")

    if get(address[4]):
        print(get(address[4]))
    else:
        print("плановая ошибка")

    if get(address[5]):
        print(get(address[5]))
    else:
        print("ошибка с получением комментария по id")

    if get(address[6]):
        print(get(address[6]))
    else:
        print("плановая ошибка")

    if get(address[7]):
        print(get(address[7]))
    else:
        print("ошибка с получением постов по id тэга")

    if get(address[8]):
        print(get(address[8]))
    else:
        print("плановая ошибка")
