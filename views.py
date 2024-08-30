from main import app
from flask import render_template, flash, send_from_directory, request, redirect, url_for, make_response
from flask_mail import Mail, Message
from content import language_colors, content_language
from forms import FormEmail


#import page contents
language_colors = language_colors
content_language = content_language


#middleware to deal with all static files caching
@app.after_request
def add_cache_headers(response):
    if request.path.startswith('/static'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'  # Cache for 1 year
    return response

#main route check por language selected already on cookies if yes redirecto you to correct mainpage or to choose the lang
@app.route("/")
def index():
    lang = request.cookies.get('lang')
    if lang:
        return redirect(url_for('home', lang=lang))
    else:
        return redirect(url_for('language_select'))

#language select page
@app.route("/language-select")
def language_select():
    return render_template("language_select.html")

#func to set the lang and cookie 
@app.route('/set_language/<lang>')
def set_language(lang):
    resp = make_response(redirect(url_for('home', lang=lang)))
    resp.set_cookie('lang', lang, max_age=60*60*24*7)  # 7 days
    return resp

#load mainpage  based on lang selected
@app.route("/<lang>/home")
def home(lang):
    if lang in ["en","pt-br","uk"]:
        email_form = FormEmail(content_language[lang]["contact_content"])
        return render_template(
            "home.html",
             lang=lang,
             content=content_language[lang],
             language_colors=language_colors,
             email_form=email_form
             )
    else:
        return render_template("404.html")

#route to download CV from 
@app.route("/download_cv")
def download_cv():
    return send_from_directory(directory="static", path="cv.pdf")

#send mail route
@app.route("/send_mail", methods=["POST"])
def send_mail():
    #mail confirmation or error based on lang
    lang = request.cookies.get('lang')
    
    email_form = FormEmail(request.form)

    if email_form.validate_on_submit():  

        contact_name = email_form.contact_name.data
        contact_email = email_form.contact_email.data
        subject = email_form.subject.data
        message = email_form.message.data

        mail = Mail(app)

        msg = Message(
            subject=subject,
            sender= app.config.get('MAIL_FROM'),
            recipients=[app.config.get('MAIL_FROM')]
        )
        msg.body = f"Name: {contact_name}\nEmail: {contact_email}\n\nMessage: {message}"

        try:
            mail.send(msg)
            flash(f"{content_language[lang]['messages']['success']}", "success")
        except Exception as e:
            print(e)
            flash(f"{content_language[lang]['messages']['error']}", "danger")
        
        return redirect(url_for("index"))
    else:
        flash(f"{content_language[lang]['messages']['captcha']}", "danger")
        return redirect(url_for("index"))

# 404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
