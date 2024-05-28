from flask import render_template, request, redirect, url_for, session, flash
from app import app, db
from models import User, History
from werkzeug.security import generate_password_hash, check_password_hash
import yt_dlp as youtube_dl  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        session['email'] = email
        return redirect(url_for('profile'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['email'] = email
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))



def get_video_info(url):
    try:
        ydl_opts = {
            'nocheckcertificate': True,  # Ignore SSL certificate verification
            'format': 'best',  # Choose the best quality format
            'outtmpl': 'static/downloads/%(title)s.%(ext)s',  # Save videos with their original names and extensions
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)  # Download the video
            title = info['title']
            filepath = ydl.prepare_filename(info)  # Get the full path to the downloaded file
            return {'title': title, 'url': url, 'filepath': filepath}
    except Exception as e:
        print("Error:", e)
        return None

    
    

from flask import send_file

@app.route('/download', methods=['POST'])
def download():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        url = request.form['url']
        video_info = get_video_info(url)
        if video_info:
            history = History(video_title=video_info['title'], video_url=video_info['url'], user=user)
            db.session.add(history)
            db.session.commit()
            
            # Construct the path to the downloaded video file
            filepath = video_info['filepath']
            
            # Send the file as a response with appropriate headers
            return send_file(filepath, as_attachment=True)
        else:
            flash('Failed to retrieve video information. Please try again.')
            return redirect(url_for('profile'))
    return redirect(url_for('login'))

