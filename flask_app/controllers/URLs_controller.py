from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.URL_model import URL


@app.route('/search', methods=['POST'])
def search():
    if not URL.validate(request.form):
        return redirect('/')
    data = {
        **request.form,
        'user_id': session["user_id"]
    }
    URL.create_url(data)
    return redirect('/welcome')
