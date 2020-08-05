from wtforms import Form, StringField,FieldList, IntegerField, BooleanField, DateTimeField, validators, ValidationError

class PostDemoArticleForm(Form):
    article_title = StringField('article_title', [validators.DataRequired()])
    article_body = StringField('article_body', [validators.DataRequired()])