#coding:utf-8
from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,SubmitField

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@localhost/luojianmei'
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='luo_h'

db = SQLAlchemy(app)

#定义模型类-作者
class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True)
    email = db.Column(db.String(64))
    au_book = db.relationship('Book',backref='author')
    def __str__(self):
        return 'Author:%s' %self.name

#定义模型类-书名
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer,primary_key=True)
    info = db.Column(db.String(32),unique=True)
    leader = db.Column(db.String(32))
    au_book = db.Column(db.Integer,db.ForeignKey('author.id'))
    def __str__(self):
        return 'Book:%s,%s'%(self.info,self.leader)



#创建表单类，用来添加信息
class Append(FlaskForm):
    au_info = StringField(validators=[DataRequired()])
    bk_info = StringField(validators=[DataRequired()])
    bk_leader = StringField(validators=[DataRequired()])
    #bk_au_book = IntegerField(validators=[DataRequired()])
    submit = SubmitField(u'添加')


@app.route('/',methods=['GET','POST'])
def index():
    #查询所有作者和书名信息
    author = Author.query.all()
    book = Book.query.all()
    #创建表单对象
    form = Append()
    if form.validate_on_submit():
        flag = 1
        #获取表单输入数据
        wtf_au = form.au_info.data
        wtf_bk_info = form.bk_info.data
        wtf_bk_leader = form.bk_leader.data
        #wtf_bk_au_book = form.bk_au_book.data
        #把表单数据存入模型类
        db_au = Author(name=wtf_au)
        db_bk_info = Book(info=wtf_bk_info,leader = wtf_bk_leader)
        #db_bk_au_book = Book(au_book = wtf_bk_au_book)
        author = Author.query.all()
        print(db_au)
        print(author)
        for au in author:
            if au.name == db_au:
                print("------------------:")
                flag = 0
        if flag:
            #提交会话
            db.session.add_all([db_au,db_bk_info])
            db.session.commit()
        #添加数据后，再次查询所有作者和书名信息
        author = Author.query.all()
        book = Book.query.all()
        return render_template('index.html',author=author,book=book,form=form)
    else:
        if request.method=='GET':
            render_template('index.html', author=author, book=book,form=form)
    return render_template('index.html',author=author,book=book,form=form)


#删除作者
@app.route('/delete_author<id>')
def delete_author(id):
    #精确查找对应的作者信息
    au = Author.query.filter_by(id=id).first()
    db.session.delete(au)
    db.session.commit()
    #直接重定向到index视图函数
    return redirect(url_for('index'))

#删除书名
@app.route('/delete_book<id>')
def delete_book(id):
    #精确查询需要删除的书名id
    bk = Book.query.filter_by(id=id).first()
    db.session.delete(bk)
    db.session.commit()
    #直接重定向到index视图函数
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    #生成数据
    au_xi = Author(name='我吃西红柿',email='xihongshi@163.com')
    au_qian = Author(name='萧潜',email='xiaoqian@126.com')
    au_san = Author(name='唐家三少',email='sanshao@163.com')
    bk_xi = Book(info='吞噬星空',leader='罗峰',au_book=1)
    bk_xi2 = Book(info='寸芒',leader='李杨',au_book=1)
    bk_qian = Book(info='飘渺之旅',leader='李强',au_book=2)
    bk_san = Book(info='冰火魔厨',leader='融念冰',au_book=3)
    #把数据提交给用户会话
    db.session.add_all([au_xi,au_qian,au_san,bk_xi,bk_xi2,bk_qian,bk_san])
    #提交会话
    db.session.commit()
    print(app.url_map)
    app.run()
