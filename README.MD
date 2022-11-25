В SQL базе данных есть продукты и категории. Одному продукту может соответствовать много категорий,
в одной категории может быть много продуктов.

Напишите HTTP API через которое можно получить:

список всех продуктов с их категориями,
список категорий с продуктами,
список всех пар «Имя продукта – Имя категории».

Если у продукта нет категорий, то он все равно должен выводиться. Если у категории нет продуктов,
то она все равно должна выводиться.

Проект должен содержать docker-compose.yml файл, через который можно запустить сервис
и проверить его работу.

---
У проекта присутствует главная страница. На которой можно перегенерировать и очистить таблицы в БД.

API Endpoints:

https://api.postman.com/collections/16322195-311aaa39-974f-428e-bb56-c817c1d03317?access_key=PMAT-01GJREHEHWK95910W8Q5Q3T1JW

В БД генерируется 3 таблицы.

Product - 50 значений

Category - 10 значений

products_categories - для связи m-t-m. Для каждого продукта с id от 1 до 45 - от 1 до 3 связей с таблицей Категории с id от 1 до 9.
В Категории c id=10 нет Продуктов.


```http://{{host}}/api/products/id``` - возвращает продукт с id (ид и имя, ссылка)

```http://{{host}}/api/products``` - возвращает все продукты (ид и имя, ссылка)

```http://{{host}}/api/products/all``` - возвращает все продукты с их категориями (ид, имя продукта, ид и имя категории).

Выполняется LEFT JOIN для таблиц к таблице Продукты
```
SELECT 
        p.id, p.prod_name, c.id, c.cat_name 
  FROM product p
            LEFT JOIN products_categories pc ON p.id = pc.product_id 
            LEFT JOIN category c ON pc.category_id = c.id
```
```http://{{host}}/api/products/1/categories``` - возвращает все категории для продукта с id



```http://{{host}}/api/categories/1``` - возвращает категорию с id (ид и имя, ссылка)

```http://{{host}}/api/categories``` - возвращает все категории (ид и имя, ссылка)

```http://{{host}}/api/categories/all``` - возвращает все категории с их продуктами (ид, имя продукта, ид и имя категории).

Выполняется LEFT и RIGHT JOIN
```
SELECT 
        p.id, p.prod_name, c.id, c.cat_name 
  FROM product p
            LEFT JOIN products_categories pc ON p.id = pc.product_id 
            RIGHT JOIN category c ON pc.category_id = c.id
```
```http://{{host}}/api/categories/10/products``` - возвращает все продукты для категории с id

```http://{{host}}/api/alldata``` - Возвращает все продукты со своей категории. Есть как пустые продукты, так и пустые категории

Выполняется LEFT и FULL JOIN
```
SELECT 
        p.id, p.prod_name, c.id, c.cat_name 
  FROM product p
            LEFT JOIN products_categories pc ON p.id = pc.product_id 
            FULL JOIN category c ON pc.category_id = c.id
```

К заданию написаны юнит-тесты. Присутсвует файл env.example. Его необходимо положить в контейнер.