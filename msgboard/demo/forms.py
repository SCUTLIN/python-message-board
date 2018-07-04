#!/usr/bin/env python
# coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, \
    SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp


class UserStatus:
    USER_STATUS_QUIT = 0
    USER_STATUS_KEEP = 1


class IndexForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'NickName must have only letters, numbers, dot or underscores')])
    nickName = StringField('Nickname', validators=[DataRequired()])
    telphone = StringField('Telphone', validators=[
        DataRequired(), Length(1, 11),
        Regexp('^1\d{10}$', 0, 'telphone must have only 11 numbers')])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    telphone = StringField('Telphone', validators=[
        DataRequired(), Length(1, 11),
        Regexp('^1\d{10}$', 0, 'telphone must have only 11 numbers')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class TouristForm(FlaskForm):
    submit_tourist = SubmitField('Visit as Tourist')


class MessageForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'NickName must have only letters, numbers, dot or underscores')])
    message = StringField('Message',
                          validators=[DataRequired(), Length(1, 1024)])
    submit = SubmitField('Submit')


class IndexSearchForm(FlaskForm):
    searchType = SelectField('Search Type',
                             coerce=int,
                             choices=[(1, 'User ID'),
                                      (2, 'User Name'),
                                      (3, 'User NickName'),
                                      (4, 'User Telphone')],
                             validators=[DataRequired()])
    searchFor = StringField('Search For', validators=[DataRequired()])
    submit = SubmitField('Search')


class ManagerSearchForm(FlaskForm):
    searchByTelphone = StringField('Search By Telphone',
                                   validators=[DataRequired()])
    submit = SubmitField('Search')


class ChangePassword(FlaskForm):
    oldPassword = PasswordField('Old Password', validators=[DataRequired()])
    newPassword = PasswordField('New Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',
                                    validators=[DataRequired()])
    submit = SubmitField('Submit')


class ManagerEditForm(FlaskForm):
    userId = HiddenField()
    name = StringField('Name', validators=[DataRequired()])
    nickName = StringField('NickName', validators=[DataRequired()])
    telphone = StringField(
        'Telphone',
        validators=[
            DataRequired(),
            Length(1, 11),
            Regexp('^1\d{10}$', 0, 'telphone must have only 11 numbers')])
    voteIncrement = IntegerField('Add Vote')
    userStatus = SelectField(
        'User Status',
        coerce=int,
        choices=[
            (UserStatus.USER_STATUS_QUIT, 'Quit'),
            (UserStatus.USER_STATUS_KEEP, 'Keep')])
    submit = SubmitField('Confirm')
