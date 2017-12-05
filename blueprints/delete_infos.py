from flask import Blueprint,redirect,url_for
from xuanhuan_story import Author,Book,app,db

delete_info = Blueprint('delete_info',__name__)

#删除作者
@delete_info.route('/delete_author<id>')
def delete_author(id):
    #查找作者id
    au = Author.query.filter_by(id=id).first()
    db.session.delete(au)
    db.session.commit()
    #直接重定向到index视图函数
    return redirect(url_for('index'))

#删除书名
@delete_info.route('/delete_book<id>')
def delete_book(id):
    #精确查询需要删除的书名id
    bk = Book.query.filter_by(id=id).first()
    db.session.delete(bk)
    db.session.commit()
    #直接重定向到index视图函数
    return redirect(url_for('index'))
