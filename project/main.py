import logging
import time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, jsonify
import datetime
import threading
import requests

app = Flask(__name__)
logger = logging.getLogger(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# har bir potok uchun qobig yartamiz
lock = threading.Lock()


def time_sleep(task):
    print(task)
    try:
        print(task)
        time_str = task.get('time')  # kelgan taskni ichidan time ovolamiz
        print(time_str)
        from model import Task

        if time_str:  # time bor yoqligini tekshiramiz
            time_obj = datetime.datetime.strptime(time_str,
                                                  '%Y-%m-%d %H:%M').timestamp()  # timeni vaqtga kein esa sekundga otqizamis
            try:
                current_time = time_obj - datetime.datetime.now().timestamp()  # kelgan timedan hozirgi vaqtni ayiramiz
                print('work time.sleep')
                print(current_time)
                time.sleep(current_time)  # ayirganda chiqanjavobga funksiyani bajaramiz
                with app.app_context():  # Flask data basega ruxsat olamiz
                    obj_task = Task.query.get(ident=task.get('id'))  # taskda kega id ga qarab task tofolamiz
                    obj_task.status = False  # statusini Truedan False ga ozgartirgan holatda
                    db.session.commit()  # data basaga saqlimiz
                # url = 'https://'
                # a = requests.get(url)
                print('end')
            except Exception as e:
                print(e)

        else:  # time yoq bolgan taqdirda error qaytarvoramiz
            return {'error': 'None'}, 400

    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/api/create-task/', methods=['POST', 'GET'])
def time_api():
    from model import Task
    if request.method == 'POST':  # request method POST bosa kevotgan datani sahranit qilamiz
        data = request.json
        task = Task(time=data['time'], desc=data['desc'], category=data['category'])

        db.session.add(task)
        db.session.commit()

        thread = threading.Thread(target=time_sleep, args=(
            [{'id': task.id, 'time': task.time}]))  # har bir task uchun alohida potok yaratamiz
        thread.start()  # keyin u potokni ishga tusharamiz

        return jsonify({'message': 'task create'}, 201)  # saxranit bogani haqida json formataga message jonatamiz

    if request.method == 'GET':  # request method GET bogan taqtirda hama tasklani json format korinishida qaytarvoramiz
        task = Task.query.all()
        task_list = [{'id': tasks.id, 'name': tasks.desc, 'status': tasks.status, 'time': tasks.time,
                      'category': tasks.category_id} for tasks in
                     task]  # har bir task bilan alohida ishlashchun for yozamiz va listni ichiga bita bita dict qoshib boramiz
        return jsonify(task_list)  # va yaratgan listimizni json formata qaytaramiz


@app.route('/api/create-category/', methods=['POST', 'GET'])
def create_cat():
    data = request.json
    from model import Category
    if request.method == 'POST':  # request method POST bosa kevotgan datani sahranit qilamiz
        cat = Category(cat_name=data['cat_name'])
        db.session.add(cat)
        db.session.commit()

        return jsonify(
            {'message': 'category create succesfuly'}, 201)  # saxranit bogani haqida json formataga message jonatamiz
    if request.method == 'GET':
        cat = Category.query.all()
        cat_list = [{'id': cats.id, 'category_name': cats.category_name} for cats in
                    cat]  # har bir cat bilan alohida ishlashchun for yozamiz va listni ichiga bita bita dict qoshib boramiz
        return jsonify(cat_list)  # va yaratgan listimizni json formata qaytaramiz


if __name__ == '__main__':
    app.run()
