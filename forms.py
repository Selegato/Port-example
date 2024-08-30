from flask_wtf import FlaskForm, RecaptchaField
from wtforms import EmailField, StringField, TextAreaField, SubmitField,\
validators as v

class FormEmail(FlaskForm):
    contact_name = StringField(
        'Name',
        [
            v.DataRequired(),
            v.Length(min=5, max=100)
        ]
    )
    
    contact_email = EmailField(
        'Email',
        [
            v.DataRequired(),
            v.Length(min=5, max=50)
        ]
    )
    
    subject = StringField(
        'Subject',
        [
            v.DataRequired(),
            v.Length(min=5, max=100)
        ]
    )
    
    message = TextAreaField(
        'Message',
        [
            v.DataRequired(),
            v.Length(min=5),
        ],
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Send')


    def __init__(self, contact_content, *args, **kwargs):
        super(FormEmail, self).__init__(*args, **kwargs)
        self.contact_name.label.text = contact_content.get('name_label', 'Name')
        self.contact_name.render_kw = {'placeholder': contact_content.get('name_placeholder', 'Your name')}
        
        self.contact_email.label.text = contact_content.get('email_label', 'Email')
        self.contact_email.render_kw = {'placeholder': contact_content.get('email_placeholder', 'name@example.com')}
        
        self.subject.label.text = contact_content.get('subject_label', 'Subject')
        self.subject.render_kw = {'placeholder': contact_content.get('subject_placeholder', 'Subject')}
        
        self.message.label.text = contact_content.get('message_label', 'Message')
        self.message.render_kw = {'placeholder': contact_content.get('message_placeholder', 'Your message here...')}
        
        self.submit.label.text = contact_content.get('btn_send', 'Send')