"""
В SQL базе данных есть продукты и категории. Одному продукту может соответствовать много категорий, 
в одной категории может быть много продуктов.

Напишите HTTP API через которое можно получить:

список всех продуктов с их категориями,список категорий с продуктами, 
список всех пар «Имя продукта – Имя категории».

Если у продукта нет категорий, то он все равно должен выводиться. Если у категории нет продуктов, 
то она все равно должна выводиться.

Проект должен содержать docker-compose.yml файл, через который можно запустить сервис 
и проверить его работу.
"""

from app import create_app


app = create_app()
