# Zakupki Hack 2
## Цель и задачи

Создать лучший интеллектуальный кластер товаров, работ и услуг (ТРУ)
с учетом всех потребностей заказчиков и участников электронных торгов.

**В рамках хакатона участникам предстоит реализовать задачи:**
1) Проанализировать бизнес-процессы, осуществляемые заказчиками и\
участниками закупок при подготовке к закупочному процессу;

2) Собрать типовые аналитические потребности заказчиков и участников закупок
при мониторинге рынка;

3) Проанализировать представленные датасеты;

4) Разобрать такие сущности, как ТРУ, товары-аналоги, сопутствующие товары.

5) Обработать характеристики ТРУ, их компоновку, страну происхождения, \
поставщиков, ценовые предложения, конкуренцию и т. д.;

6) Создать работающий прототип, с помощью которого \
можно найти необходимые ТРУ, их свойства, производителей, уровни цен и т.д.;
7) Продемонстрировать работоспособность проекта;
8) Определить возможности по масштабированию решения и следующим его
доработкам;
9) Презентовать проект.

## Решение

![scheme](https://github.com/EugGolovanov/Zakupki/blob/main/images/app-work-2.jpg)

Хост на презентации: Intel(R) Core(TM) i5-7500 CPU @ 3.40Ghz on 1 core 16 GB RAM.

Проект представляет из себя комбинаицю самых свежих практик и технологий,\
благодаря чему способен производить поиск закупок и работ параллельно с сопутсвующими товарами менее чем за пол секундуы!

Проект разработан так, что масштабируемость происходит нативно. При увеличении объема данных, скорость упадет, но совсем незначительно. Мы используем FAISS, разработку которую применяют на детекции лиц и сопоставлении им профилей на более чем 12 миллионов картинок.

Подробнее - [FAISS: Быстрый поиск лиц и клонов на многомиллионных данных](https://habr.com/ru/company/dentsuRU/blog/509204/)

Если в наших руках окажутся данные с парами вместе с A купил B, то мы сможем значительно улучшить качество ранжирования.

Приложение адаптировано как под стационарные компьютеры, ноутбуки,\
так и под мобильные телефоны. Используется фреймворк streamlit.

Мы производим оптимизацию потребления ресурсов диска при работе с эмбеддингами, благодаря использованию бинарного формата feather. 900 мб на диске и около 5 сек на прочтение. Эмбеддинги (1 миллион строк * 312 dim) занимают в памяти, в fp16 порядка 600-700мб.

Если бы хранили эмбеддинги в csv, то время прочтения составило ~30 сек, а объем на диске порядка 3-4 гб.

В качестве моделей используются BERT (rubert-tiny2, production ready) и Catboost Classifier.

Таким образом проект портебляет порядка 3-4 гб оперативной памяти, и способен выполняться на одном ядре CPU без использования GPU. Все в купе позволяет экономить на содержании продукта, что немало важно при реальном использовании.


## Полезное:
[Данные](https://github.com/EugGolovanov/Zakupki/tree/main/data)\
[Как запустить локально (on Windows 11)](https://github.com/EugGolovanov/Zakupki/tree/main/streamlit-app)\
[Кодовая база для обучения](https://github.com/EugGolovanov/Zakupki/tree/main/notebooks)
