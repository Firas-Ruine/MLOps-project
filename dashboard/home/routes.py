# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from dashboard.home import blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/youtube', methods=['GET', 'POST'])
@login_required
def youtube():
    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url')
        if youtube_url:
            # Add prediction logic here
            flash(f"Received YouTube URL: {youtube_url}", "success")
            return render_template('home/youtube.html', segment='youtube')
        else:
            flash("Please enter a valid YouTube URL.", "danger")
    return render_template('home/youtube.html', segment='youtube')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
