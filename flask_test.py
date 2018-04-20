from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import datetime
import config

app = Flask ( __name__ )
app.config.from_object ( config )

db = SQLAlchemy ( app )

db.create_all ()


class Student ( db.Model ):
    __tablename__ = 'student'
    id = db.Column ( db.Integer, primary_key=True )
    name = db.Column ( db.String ( 20 ) )


class Blog ( db.Model ):
    __tablename__ = 'Blog'
    id = db.Column ( db.Integer, primary_key=True )
    title = db.Column ( db.String ( 20 ) )
    content = db.Column ( db.Text )
    studentid = db.Column ( db.Integer )
    createdate = db.Column ( db.Date )


# 主页
@app.route ( '/', methods=['GET', 'POST'] )
def home():
    lst_blog = Blog.query.join ( Student, Student.id == Blog.studentid ).add_columns ( Blog.id, Blog.title,
                                                                                       Student.name,
                                                                                       Blog.createdate ).all ()

    student = Student ()
    id = None
    name = None
    if 'id' in session:
        id = session.get ( 'id' )
        name = session.get ( 'name' )
    content = {'id': id, 'name': name, 'lst_blog': lst_blog}
    return render_template ( 'home.html', **content )


# 登录页面
@app.route ( '/signin', methods=['GET'] )
def signin_form():
    return render_template ( 'form.html' )


# 登录提交
@app.route ( '/signin', methods=['POST'] )
def signin():
    id = request.form['id'].strip ();
    name = request.form['name'].strip ();
    filters = {Student.id == id, Student.name == name}
    student = Student.query.filter ( *filters ).first ()
    if (student != None):
        session['id'] = student.id
        session['name'] = student.name
        return redirect ( url_for ( 'home' ) )
    return render_template ( 'form.html', message='登录失败' )


# 注册页面
@app.route ( '/register', methods=['GET'] )
def register_form():
    return render_template ( 'register.html' )


# 注册提交
@app.route ( '/register', methods=['POST'] )
def register():
    id = request.form['id'].strip ();
    name = request.form['name'].strip ();
    filters = {Student.id == id, Student.name == name}
    try:
        stdent = Student ( id=id, name=name )
        db.session.add ( stdent )
        # 事务
        db.session.commit ()
    except Exception:
        return render_template ( 'register.html', message='注册失败' )
    return render_template ( 'form.html' )


# 退出登录
@app.route ( '/loginout', methods=['GET'] )
def loginout():
    session.clear ()
    return redirect ( url_for ( 'home' ) )


# 发布博客页面
@app.route ( '/WriteBlog', methods=['GET'] )
def WriteBlog_form():
    if 'id' not in session:
        return redirect ( url_for ( 'signin_form' ) )
    id = session.get ( 'id' )
    name = session.get ( 'name' )
    content = {'id': id, 'name': name}
    return render_template ( 'WriteBlog.html', **content )


# 发表博客提交
@app.route ( '/WriteBlog', methods=['POST'] )
def WriteBlog():
    if 'id' not in session:
        return redirect ( url_for ( 'signin_form' ) )
    title = request.form['title'].strip ()
    content = request.form['content'].strip ()
    try:
        blog = Blog ( id=random.randint ( 10, 20 ), title=title, content=content,
                      studentid=str ( session.get ( 'id' ) ), createdate=datetime.datetime.now () )
        db.session.add ( blog )
        # 事务
        db.session.commit ()
        return redirect ( url_for ( 'home' ) )
    except Exception:
        return render_template ( 'WriteBlog.html', message='发布失败' )


@app.route ( '/BlogDetails/<blogid>', methods=['GET'] )
def getBlogDetails(blogid):
    blogdetails = Blog.query.join ( Student, Student.id == Blog.studentid ).filter ( Blog.id == blogid ).add_columns (
        Blog.id, Blog.title, Student.name, Blog.content, Blog.createdate ).first ()
    student = Student ()
    id = None
    name = None
    if 'id' in session:
        id = session.get ( 'id' )
        name = session.get ( 'name' )
    content = {'id': id, 'name': name, 'blogdetails': blogdetails}
    return render_template ( 'BlogDetails.html', **content )


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run ( host='0.0.0.0', port=9868, debug=True )
