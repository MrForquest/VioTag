from all_resources import *
from requests import get

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