#coding=utf-8
import unittest
from xuanhuan_story import *
class Database_test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://luojian:123456@localhost:3306/test'
        self.app = app
        db.create_all()
        print("不写单元测试的程序猿不是一只好猿！")

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #测试代码
    def test_append_data(self):
        au = Author(name='luojian')
        bk = Book(info='python')
        db.session.add_all([au,bk])
        db.session.commit()
        author = Author.query.filter_by(name='luojian').first()
        book = Book.query.filter_by(info='python').first()
        #断言数据存在
        self.assertIsNotNone(author)
        self.assertIsNotNone(book)
