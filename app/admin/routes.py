from app.admin import admin, maildaemon
import os
import imghdr
from dotenv import load_dotenv
from flask import (render_template, flash, redirect, url_for, request, abort)
from werkzeug.utils import secure_filename
from flask_login import (current_user, login_required, login_user, logout_user, confirm_login)
from datetime import datetime
from .models import User, login_manager, da, db
from .forms import PostForm, EmailForm, LoginForm, JobForm
from app.home.models import Posts, Jobs
from flask_mail import Message, Mail


load_dotenv()
JOB_IMAGES = os.environ.get('JOB_IMAGES')
IMAGE_EXTENSIONS = os.environ.get('IMPAGE_EXTENSIONS')


@admin.route('/admin', methods=['GET'])
def index():
    return render_template("admin/index.html")


@admin.route('/admin/login', methods=['GET'])
def login():
    return render_template("admin/login.html")


@admin.route('/admin/register', methods=['GET'])
def register():
    return render_template("admin/register.html")


@admin.route('/logout', methods=['GET'])
def logout():
    return render_template("admin/index.html")


@admin.route('/admin/inbox', methods=['GET'])
def inbox():
    return render_template("admin/mailbox.html")


@admin.route('/admin/compose', methods=['GET', 'POST'])
def mail_compose():
    forma = EmailForm()
    if request.method == 'POST':
        compose_mail()
        return render_template('admin/mailbox-compose.html', success=True)
    else:
        pass
        #    MAP_BOX_KEY = os.environ.get('MAP_BOX_KEY')
        return render_template('admin/mailbox-compose.html', form=forma)


@admin.route('/admin/mail', methods=['GET'])
def mail():
    return render_template("admin/mailbox-view.html")


@admin.route('/admin/lock', methods=['GET'])
def lock():
    form = LoginForm()
    return render_template("admin/lock.html", now=datetime.utcnow(), form=form)


@admin.route('/admin/recovery', methods=['GET'])
def password_recovery():
    return render_template("admin/password-recovery.html")


@admin.errorhandler(404)
def page_not_found(error):
    return render_template('admin/404.html'), 404


@admin.errorhandler(500)
def internal_error(error):
    return render_template('admin/500.html'), 500


@admin.route('/admin/files', methods=['GET'])
def file_manager():
    return render_template("admin/file-manager.html")


@admin.route('/admin/analytics', methods=['GET'])
def analytics():
    return render_template("admin/analytics.html")


@admin.route('/admin/blog', methods=['GET'])
def blogstats():
    return render_template("admin/blog.html")


@admin.route('/admin/create_post', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author='Admin', slug=form.slug.data,
                     subtitle=form.subtitle.data, category_id=form.category.data)
        da.session.add(post)
        da.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/blog_create.html', form=form)


@admin.route('/admin/pw', methods=['GET'])
def password_meter():
    return render_template("admin/password-meter.html")


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def compose_mail():
    forma = EmailForm()
    # emailer = forma.email.data
    # name = request.args.get('name')
    if request.method == 'POST':
        if forma.validate() == False:
            flash('All fields are required.')
            return render_template('admin/mailbox-compose.html', form=forma)
        else:
            msg = Message(forma.subject.data, sender=('Shout from Dike', 'shout@dikedim.com'),
                          recipients=forma.rcpt_email.data)
            msg.body = """
                  From: %s &lt;%s&gt;
                  %s
                  """ % ('shout@dikedim.com', forma.rcpt_email.data, forma.message1.data)
            # msg.attach(forma.attachment.data.filename, )
            maildaemon.send(msg)
            # confirm_mail()
            return render_template('admin/mailbox-compose.html', success=True)

    elif request.method == 'GET':
        return render_template('admin/mailbox-compose.html', form=forma)


@admin.route('/admin/addjob', methods=['GET', 'POST'])
def addjob():
    form = JobForm()
    #listStat = [('1', 'Mobile'), ('2', 'Video'), ('3', 'Photo'), ('4', 'Web'), ('5', 'Desktop')]
    #form.process()
    if form.validate_on_submit():
        #upload_image()
        m = request.files['photo']
        m.save(os.path.join(JOB_IMAGES, secure_filename(m.filename)))
        photo_ = request.form.get('photo')
        filename = secure_filename(form.photo.data.filename)
        photos = form.photo.data.save(JOB_IMAGES + filename)
        job = Jobs(title=form.title.data, content=form.content.data, link=form.link.data,
                   photo=photos, jobtype_id=form.category.data)
        db.session.add(job)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/jobs.html', form=form)


#def upload_image():
#    m = JobForm()
#    job_image = request.files['photo']
#    filename = secure_filename(job_image.filename)
#    if filename != '':
#        file_extension = os.path.splitext(filename)[1]
#        if file_extension not in 'IMAGE_EXTENSIONS' or file_extension != validate_(job_image.stream):
#            abort(400)
#        job_image.save(os.path.join('JOB_IMAGES', filename))
#        # filename = secure_filename(m.photo.data.filename)
#        # m.photo.data.save(JOB_IMAGES + filename)
#        print('file uploaded')
#    return redirect(url_for('addjob'))
#
#
#def validate_(stream):
#    header = stream.read(512)
#    stream.seek(0)
#    format_ = imghdr.what(None, header)
#    if not format_:
#        return None
#    return '.' + (format_ if format_ != 'jpeg' else 'jpg')

#
#def upload():
#    f = request.files['photo']
#    f.save(secure_filename(f.filename))
#    return 'file uploaded successfully'
#