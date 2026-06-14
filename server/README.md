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
> uvicorn app.main:app

