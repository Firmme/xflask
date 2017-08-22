# -- coding:utf-8 --
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'自动登录')
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    email = StringField(u'邮箱', validators=[
        DataRequired(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[
        DataRequired(), Length(1.64), Regexp('[A-Za-z][A-Za-z0-9_-]*$', 0,
                                             'user' 'num')])
    password = PasswordField(u'密码', validators=[DataRequired()])
    password2 = PasswordField(u'确认密码', validators=[
        DataRequired(), EqualTo('password', message=u'两次输入的密码不一致!')])

    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮件地址已被注册!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被使用!')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[DataRequired()])
    password2 = PasswordField(
            u'确认密码', validators=[
                DataRequired(), EqualTo(
                        'password', message=u'两次输入的密码必须一致')])
    submit = SubmitField(u'修改密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(u'邮件地址', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField(u'重设密码')


class PasswordResetForm(FlaskForm):
    email = StringField(u'邮件地址', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(u'新密码', validators=[DataRequired()])
    password2 = PasswordField(
            u'确认密码', validators=[
                DataRequired(), EqualTo(
                        'password', message=u'两次输入的密码必须一致')])
    submit = SubmitField(u'重设密码')

    def validate_email(self, filed):
        if User.query_by(email=filed.data).first() is None:
            raise ValidationError(u'未知的邮件地址')

class ChangeEmailForm(FlaskForm):
    email = StringField(u'新的邮件地址',validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField(u'密码',validators=[DataRequired()])
    submit = SubmitField(u'更新邮件地址')

    def validte_email(self,field):
        if User.query.filter_by(email = field.data):
            raise ValidationError(u'此邮箱已被注册!')
