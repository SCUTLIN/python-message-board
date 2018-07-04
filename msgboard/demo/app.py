#! /usr/bin/env python
# coding=utf-8
import time
from flask import render_template, session, redirect, url_for, flash
from flask.globals import request
from demo.dbmanager import DbManager
from demo.cache.redis_cache import SessionCache
from demo.forms import RegisterForm, LoginForm, MessageForm, TouristForm
from demo.log.Logger import logger
from demo.__init__ import app



@app.before_first_request
def create_session_cache():
    session_cache = SessionCache(session)
    logger.info('create session %s cache success' % session_cache.session_id)


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/rankboard', methods=['GET', 'POST'])
def rankboard():
    session_cache = SessionCache(session)
    if str(session_cache['login_success']) != str(True):
        return redirect(url_for('login'))
    try:
        rank_board = DbManager.get_rank(10)
    except:
        logger.exception('get active top10 failed')
    return render_template('rankboard.html', rankBoard=rank_board)


@app.route('/msgboard', methods=['GET', 'POST'])
def msgboard():
    session_cache = SessionCache(session)
    if str(session_cache['login_success']) != str(True):
        return redirect(url_for('login'))

    curr_page = request.args.get('page', 1, type=int)
    pre_page = 10
    try:
        form = MessageForm()
        if form.validate_on_submit():
            nickname = str(form.name.data)
            message = str(form.message.data)
            time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            time_float = time.time()
            DbManager.submit_msg(nickname, message, time_stamp, time_float)
    except:
        logger.exception('submit message failed')

    total_page = DbManager.db_msg_total_page(pre_page)
    msg_board = DbManager.get_msg(curr_page, pre_page)
    pageInfo = {'curr': curr_page, 'total': total_page, 'pre': pre_page}
    return render_template(
        'msgboard.html',
        form=form,
        name=session_cache['name'],
        role=session_cache['role'],
        msgBoard=msg_board,
        page=pageInfo)


@app.route('/', methods=['GET', 'POST'])
def index():
    session_cache = SessionCache(session)
    if str(session_cache['login_success']) != str(True):
        return redirect(url_for('login'))

    return redirect(url_for('msgboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        telphone = long(form.telphone.data)
        if telphone is not None:
            userInfo = DbManager.find_usr_by_phone(str(telphone))
            logger.info('userInfo is %s' % str(userInfo))
            if userInfo is not None:
                flash('Telphone %s has been registered!' % telphone)
            else:
                userInfo = {
                    'name': form.name.data,
                    'nickname': form.nickName.data,
                    'telphone': form.telphone.data,
                    'password': form.password.data,
                    'role': 'User'
                }
                DbManager.register(userInfo)
                logger.info('insert userInfo is %s' % str(userInfo))
                flash('Register %s success!' % telphone)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session_cache = SessionCache(session)
    form1 = LoginForm()
    form2 = TouristForm()
    if form1.validate_on_submit():
        telphone = str(form1.telphone.data)
        password = str(form1.password.data)
        userInfo = DbManager.find_usr_by_phone(str(telphone))
        if userInfo is not None:
            if password == userInfo.get('password'):
                session_cache.add_map(userInfo)
                session['login_success'] = True
                session_cache['login_success'] = True
                flash('Login Success')
                return redirect(url_for('index'))
        flash('Telphone or password error')
    elif form2.validate_on_submit():
        userInfo = {
            'name': 'Tourist',
            'nickname': 'Tourist',
            'telphone': '00000000000',
            'password': '123',
            'role': 'Tourist'
        }
        session_cache.add_map(userInfo)
        session['login_success'] = True
        session_cache['login_success'] = True
        flash('Welcome Tourist')
        return redirect(url_for('index'))
    return render_template('login.html', form1=form1, form2=form2)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=10086, debug=True)
