---
tags: [Import-5be1]
title: README
created: '2025-12-24T18:21:21.641Z'
modified: '2026-06-05T03:58:55.846Z'
---

## Для запуска нужно проделать следущие действия
- установить виртуальную среду:
> pip install venv
- создать venv в папке сервера
> python -m venv {virt_name} 
- Активировать виртуальную среду (пр. virt)
> virt\Scripts\activate 
- Установить зависимости из файла requiments.txt
>  pip install -r requirements.txt
- Запуск сервера
> uvicorn app.main:app --reload

