# -- coding:utf-8 --
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, \
    PasswordResetForm, PasswordResetRequestForm, ChangeEmailForm
from . import auth
from .. import db, email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误!')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash(u'您已经退出登录!')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        email.send_email(user.email, 'cofirm',
                         'auth/email/confirm', user=user, token=token)
        flash(u'注册成功去邮箱确认吧')
        return redirect((url_for('main.index')))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    email.send_email(current_user.email, 'Confirm your account',
                     'auth/email/confirm', user=current_user,
                     token=token)
    flash(u'新的注册邮件已经发送至您的邮箱,上一封邮件将失效.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u'注册成功!')
    else:
        flash(u'地址无效或已过期!')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash(u'您的密码已经更新,请用新密码登录!')
            return redirect(url_for('main.index'))
        else:
            flash(u'密码错误')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            email.send_email(user.email, u'重设密码', 'auth/email/reset_password',
                             token=token, user=user, next=request.args.get('next'))
        flash(u'重设密码的邮件已经发送至您的邮箱,请到您的邮箱查找!')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash(u'您的密码已重设!')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            email.send_email(new_email, u'认证您的邮箱地址', 'auth/email/change_email',
                             user=current_user, token=token)
            flash(u'认证邮件已经发送至您的邮箱,请查收')
            return redirect(url_for('main.index'))
        else:
            flash(u'邮件或密码错误')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change_email/token')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash(u'你的邮箱已变更!')
    else:
        flash(u'无效请求!')
    return redirect(url_for('main.index'))
