from app import User, Movie  # 导入模型类
user = User(name='Grey Li')  # 创建一个 User 记录
m1 = Movie(title='Leon', year='1994')  # 创建一个 Movie 记录
m2 = Movie(title='Mahjong', year='1996')  # 再创建一个 Movie 记录
db.session.add(user)  # 把新创建的记录添加到数据库会话
db.session.add(m1)
db.session.add(m2)
db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可