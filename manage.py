#coding:utf-8
from xuanhuan_story import app,db,Author,Book
from flask_script import Manager

manager = Manager(app)

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

#蓝图导入及注册
from blueprints.delete_infos import delete_info
app.register_blueprint(delete_info,url_prefix='')

print(app.url_map)
manager.run()
