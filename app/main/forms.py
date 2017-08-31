# -- coding:utf-8 --
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField(u'您的名字是?', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class EditProfileForm(FlaskForm):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'家乡', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField(u'邮件', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              u' 用户名只允许输入字母 '
                                              u'数字,点或下划线')])
    confirmed = BooleanField(u'用户认证')
    role = SelectField(u'用户级别', coerce=int)
    name = StringField(u'真实姓名 ', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'签名')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮件已被注册.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'此用户名已被注册.')


class PostForm(FlaskForm):
    body = PageDownField(u"最近发生了什么?", validators=[DataRequired()])
    submit = SubmitField(u'发布')
