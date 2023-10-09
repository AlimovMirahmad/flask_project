from main import db


class Category(db.Model):  # category model yaratamiz
    id = db.Column(db.Integer, primary_key=True)  # unda id va name fieldlari boladi
    category_name = db.Column(db.String(100), nullable=False)

    def __init__(self, cat_name):  # yaratish uchun esa faqat name kerak boladi
        self.category_name = cat_name


class Task(db.Model):  # taskning modelini yaratamiz
    id = db.Column(db.Integer, primary_key=True)  # unda id desc time status va cat_idsi boladi
    desc = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, desc, time, category):  # task yaratish uchun desc time va category kerak boladi
        self.desc = desc
        self.time = time
        self.category_id = category


# class TaskHistory(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    task_id = db.Column(db.Integer, db.ForignKey('task.id'))
#    response = db.column(db.Text, nullable=False)
#    status_code = db.Column(db.Integer)


db.create_all()
