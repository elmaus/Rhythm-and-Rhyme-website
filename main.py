
import os
import random
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin
from werkzeug.utils import secure_filename
from flask_fontawesome import FontAwesome

import mtime

app = Flask(__name__)
db = SQLAlchemy(app)
fa = FontAwesome(app)

image_dir = os.path.join(app.static_folder, 'images')
os.makedirs(image_dir, exist_ok=True)

gallery_dir = os.path.join(app.static_folder, 'gallery')
os.makedirs(gallery_dir, exist_ok=True)

cont_profile = os.path.join(app.static_folder, 'contender_profile')
os.makedirs(cont_profile, exist_ok = True)

judges_profile = os.path.join(app.static_folder, 'judges_prifile')
os.makedirs(judges_profile, exist_ok = True)

member_profile = os.path.join(app.static_folder, 'member_profile')
os.makedirs(member_profile, exist_ok = True)

video_dir = os.path.join(app.static_folder, 'videos')
os.makedirs(video_dir, exist_ok=True)

video_entry_dir = os.path.join(app.static_folder, 'video_entry')
os.makedirs(video_entry_dir, exist_ok=True)

audio_dir = os.path.join(app.static_folder, 'audios')
os.makedirs(audio_dir, exist_ok=True)

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'mp4', 'mov', 'gif', 'png']


app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rhythmandrhymegroup.mysql.pythonanywhere-services.com'
#app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = '1LoveCodin6'

login_manager = LoginManager(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    kind = db.Column(db.String(50))
    section = db.Column(db.String(50))

class Members(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    title = db.Column(db.String(50))
    division = db.Column(db.String(50))
    admission = db.Column(db.String(50))
    smule = db.Column(db.String(50))
    group = db.Column(db.String(50))
    location = db.Column(db.String(100))
    birthday = db.Column(db.String(50))
    fav_song = db.Column(db.String(500))
    picture = db.Column(db.String(1000))
    bio = db.Column(db.String(1000))

class Contenders(db.Model):
    __tablename__ = "contender"
    id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.String(50))
    group = db.Column(db.String(50))
    smule = db.Column(db.String(50))
    picture = db.Column(db.String(100))

class Judge(db.Model):
    __tablename__ = "judge"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    picture = db.Column(db.String(50))
    bio = db.Column(db.String(1000))

class Entry(db.Model):
    __tablename__ = "entry"
    id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(50))
    link = db.Column(db.String(1000))
    frame = db.Column(db.String(1000))
    submitted = db.Column(db.String(50))
    ja = db.Column(db.String(20))
    jb = db.Column(db.String(20))
    jc = db.Column(db.String(20))
    jd = db.Column(db.String(20))
    je = db.Column(db.String(20))
    comment1 = db.Column(db.String(1000))
    comment2 = db.Column(db.String(1000))

class BackupEntry(db.Model):
    __tablename__ = "backupentry"
    id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.String(20))
    link = db.Column(db.String(1000))
    deleted = db. Column(db. String(100))
    ja = db.Column(db.String(50))
    jb = db.Column(db.String(50))
    jc = db.Column(db.String(50))
    jd = db.Column(db.String(50))
    je = db.Column(db.String(50))

class CurrentComp(db.Model):
    __tablename__ = "currentcomp"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    tag = db.Column(db.String(1000))
    round = db.Column(db.Integer)
    banner = db.Column(db.String(1000))
    deadline = db.Column(db.String(50))
    announce = db.Column(db.String(50))
    show = db.Column(db.String(10))
    crit1 = db.Column(db.String(200))
    crit2 = db.Column(db.String(200))
    crit3 = db.Column(db.String(200))
    per1 = db.Column(db.String(10))
    per2 = db.Column(db.String(10))
    per3 = db.Column(db.String(10))
    ja = db.Column(db.String(20))
    jb = db.Column(db.String(20))
    jc = db.Column(db.String(20))
    jd = db.Column(db.String(20))
    je = db.Column(db.String(20))

class Picture(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key = True)
    picture = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    category = db.Column(db.String(50))


class Result:
    def __init__(self, badge, name, a, b, c, d, e, total):
        self.badge = badge
        self.name = name
        self.ja = a
        self.jb = b
        self.jc = c
        self.jd = d
        self.je = e
        self.total = total
        self.rank = 1

def scoreinfo(name, per1, per2, per3, a, b, c, d, e):
    name = name
    a = list(map(lambda x: float(x), a.split('-')))
    b = list(map(lambda x: float(x), b.split('-')))
    c = list(map(lambda x: float(x), c.split('-')))
    d = list(map(lambda x: float(x), d.split('-')))
    e = list(map(lambda x: float(x), e.split('-')))
    ja = ["%.2f" % float(a[0]*per1), "%.2f" % float(a[1]*per2), "%.2f" % float(a[2]*per3)]
    jb = ["%.2f" % float(b[0]*per1), "%.2f" % float(b[1]*per2), "%.2f" % float(b[2]*per3)]
    jc = ["%.2f" % float(c[0]*per1), "%.2f" % float(c[1]*per2), "%.2f" % float(c[2]*per3)]
    jd = ["%.2f" % float(d[0]*per1), "%.2f" % float(d[1]*per2), "%.2f" % float(d[2]*per3)]
    je = ["%.2f" % float(e[0]*per1), "%.2f" % float(e[1]*per2), "%.2f" % float(e[2]*per3)]

    info = {"name":name, "ja":ja, "jb":jb, "jc":jc, "jd":jd, "je":je}
    return info


def rank(a, b, reverse=False):
    result = None

    list1 = b
    if reverse == False:
        list1.sort(reverse=True)
    else:
        list1.sort()

    list2 = list(dict.fromkeys(list1))
    for i in range(len(list2)):
        if a == list2[i]:
            result = i+1

    return result


def allowed_file(filename):
    ext = filename.split('.')[1].lower()
    if ext in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

def get_smule_frame(text):
    first = text.split(" ")[4]
    iframe = first.split('"')[1]
    return iframe

def get_smule_link(text):
    first = text.split("www.smule.com")
    link = first[-1]
    return link

def get_filename(text):
    a = random.randint(0, 99)
    b = random.randint(0, 99)
    c = random.randint(0, 99)
    d = "{}-{}-{}-{}".format(text, a, b, c)
    return d

@app.route('/')
def home():
    title='HOME - Rhythm and Rhyme'
    return render_template('index.html', title=title)

@app.route('/about')
def about():
    title='ABOUT - Rhythm and Rhyme'
    return render_template('about.html', title=title)

@app.route('/event', methods=['GET'])
def event():
    title="EVENT - Rhythm and Rhyme"
    comp = CurrentComp.query.filter_by(id=1).first()
    return render_template('event-page.html', title=title, comp=comp)

@app.route('/members', methods=['GET'])
def members():
    title='MEMBERS'
    members = 'members'
    return render_template('index.html', title=title, members=members)

@app.route('/top_5', methods=['GET'])
def top_5():
    title = 'TOP 5 - Rhythm and Rhyme'
    top = Members.query.filter_by(division='Top 5').all()
    return render_template('division/top5.html', title=title, top=top)

@app.route('/officer', methods=['GET'])
def officer():
    title = 'OFFICERS - Rhythm and Rhyme'
    officer = Members.query.filter_by(division='Officer').all()
    return render_template('division/officer.html', title=title, officers=officer)

@app.route('/pioneer', methods=['GET'])
def pioneer():
    title = 'PIONEERS - Rhythm and Rhyme'
    pioneer = Members.query.filter_by(division='Pioneer').all()
    return render_template('division/pioneer.html', title=title, pioneers=pioneer)

@app.route('/loyal', methods=['GET'])
def loyal():
    title = 'LOYALS - Rhythm and Rhyme'
    loyal = Members.query.filter_by(division='Loyal').all()
    return render_template('division/loyal.html', title=title, loyal=loyal)

@app.route('/comrade', methods=['GET'])
def comrade():
    title = 'FAMILY - Rhytm and Rhyme'
    comrade = Members.query.filter_by(division='Member').all()
    return render_template('division/comrade.html', title=title, comrade=comrade)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "LOGIN - Rhythm and Rhyme"
    user = User.query.filter_by(username=request.form.get("username")).first()
    pw = request.form.get("password")

    if request.method == 'POST':
        if user and user.password == pw:
            login_user(user, remember=request.form.get("check"))
            if current_user.kind == "admin":
                pass
            if current_user.kind == "registrar":
                pass
            if current_user.kind == "judge":
                return redirect(url_for("score_sheet"))
        else:
            info = "Login Failed!"
            message = " Please ask any Rythm and Rhyme officer for assistance."
            return render_template('responses/response.html', info=info, message=message)

    return render_template('registration/login.html', title=title)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/member_registration', methods=["GET", "POST"])
def member_registration():
    title = 'NEW MEMBERS REGISTRATION - Rhytm and Rhyme'
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    day = [d for d in range(1, 32)]


    if request.method == 'POST':
        name = request.form.get('name')
        old = Members.query.filter_by(name=name).first()
        smule = request.form.get('smule')
        group = request.form.get('group')

        month = request.form.get('month')
        day = request.form.get('day')
        birthday = '{} {}'.format(month, day)
        song = request.form.get('song')
        location = request.form.get('location')
        bio = request.form.get('bio')

        title = 'Member'
        division = 'Pending'
        admission = mtime.now()

        if 'file' not in request.files:
            return render_template('response.html')
        file = request.files['file']
        if file.filename == '':
            return render_template('response.html')
        if file and allowed_file(file.filename):
            file_name = '{}.{}'.format(get_filename(name), file.filename.split('.')[-1])
            filename = file_name.replace(" ", "_")
            if filename and not old:
                file.save(os.path.join(member_profile, secure_filename(filename)))

                new = Members(name=name, title=title, division=division, admission=admission, smule=smule, group=group, location=location, birthday=birthday, fav_song=song, picture=filename, bio=bio)
                db.session.add(new)
                db.session.commit()

                return render_template('responses/regis_member_response.html', title='MEMBER REGISTRATION', name=name.split(' ')[0])
            else:
                info = "Registration Failed"
                message = 'Please ask any Rhythm and Rhyme officers for assistance'
                return render_template('responses/response.html', title='MEMBER REGISTRATION', info=info, message=message)

        else:
            info = "Registration Failed"
            message = 'Please ask any Rhythm and Rhyme officers for assistance'
            return render_template('responses/response.html', title='MEMBER REGISTRATION')

    return render_template('registration/member_registration.html', title=title, month=month, day=day)

@app.route("/edit_member", methods=["GET", "POST"])
def edit_member():
    title = "EDIT MEMBER INFO"
    all = Members.query.all()


    if request.method == "POST":
        if request.form.get("submit") == "edit":
            member = request.form.get("member")
            target = Members.query.filter_by(name=member).first()

            name = request.form.get("name")
            target.name = name

            title = request.form.get("title")
            target.title = title

            smule = request.form.get("smule")
            target.smule = smule

            birthday = request.form.get("birthday")
            target.birthday = birthday

            division = request.form.get("division")
            target.division = division

            admission = request.form.get("admission")
            target.admission = admission

            location = request.form.get("location")
            target.location = location

            bio = request.form.get("bio")
            target.bio = bio

            fav_song = request.form.get("fav_song")
            target.fav_song = fav_song

            file = request.files['file']
            if file.filename== "":
                pass
            if file and allowed_file(file.filename):
                file_name = "{}.{}".format(get_filename(name), file.filename.split('.')[-1])
                filename = file_name.replace(" ", "_")
                if filename:
                    os.remove("static/member_profile/{}".format(target.picture))
                    file.save(os.path.join(member_profile, secure_filename(filename)))
                    target.picture = filename


            db.session.commit()
            message = "{} info has been updated".format(name)

            return render_template("admin/edit-member-response.html", message=message)


    return render_template('admin/find_member.html', title=title, all=all)

@app.route("/delete_member", methods=["POST"])
def delete_member():
    if request.method == "POST":
        name = request.form.get("delete")
        if name == "back":
            return redirect(url_for("view_members"))
        else:
            message = "{} is deleted".format(name)
            target = Members.query.filter_by(name=name).first()
            os.remove("static/member_profile/{}".format(target.picture))
            db.session.delete(target)
            db.session.commit()
            return render_template("admin/edit-member-response.html", message=message)

@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        func = request.form.get("edit").split("-")[0]
        name = request.form.get("edit").split("-")[1]
        target = Members.query.filter_by(name=name).first()
        if func == "delete":
            return render_template('admin/delete-member-confirm.html', target=target)
        if func == "edit":
            return render_template('admin/edit_member.html', target=target)

@app.route('/view_members', methods=['GET'])
def view_members():
    title = "MEMBERS DATA - Rhythm and Rhyme"
    top5 = len(Members.query.filter_by(division="Top 5").all())
    officer = len(Members.query.filter_by(division="Officer").all())
    pioneer = len(Members.query.filter_by(division="Pioneer").all())
    loyal = len(Members.query.filter_by(division="Loyal").all())
    member = len(Members.query.filter_by(division="Member").all())
    members = Members.query.all()
    totmem = len(members)

    return render_template('admin/view-members.html', title=title, members=members, top5=top5, officer=officer, pioneer=pioneer, loyal=loyal, member=member, totmem=totmem)


@app.route("/register_judge", methods=['GET', 'POST'])
def register_judge():
    title = "JUDGE REGISTRATION FORM - Rhythm and Rhyme"
    invalid_file = " Invalid File!"
    ask = " Please ask any Rhythm and Rhyme officers for assiatance"
    reg_failed = "Registration Failed"

    if request.method == "POST":
        name = request.form.get('name')
        old = Judge.query.filter_by(name=name).first()
        username = request.form.get('username')
        password = request.form.get('password')
        bio = request.form.get('bio')

        if 'file' not in request.files:
            return render_template('responses/response.html')
        file = request.files['file']
        if file.filename == "":
            return render_template('responses/response.html', info=invalid_file, mesaage=ask)
        if file and allowed_file(file.filename):
            file_name = "{}-{}.{}".format(name, mtime.now(), file.filename.split('.')[-1])
            filename = file_name.replace(" ", "_")
            if filename and not old:
                file.save(os.path.join(judges_profile, secure_filename(filename)))

                new = Judge(name=name, username=username, password=password, picture=filename, bio=bio)
                db.session.add(new)
                db.session.commit()

                info = " Registration Success!"
                message = " Thanks for being a part of Rhythm and Rhyme competition."
                return render_template('responses/response.html', info=info, message=message)
            else:
                return render_template('responses/response.html', info=reg_failed, message=ask)
        else:
            return render_template('responses/response.html', info=invalid_file, message=ask)
    return render_template('registration/judges-registration.html', title=title)

@app.route("/edit_judges", methods=['GET', 'POST'])
def edit_judges():
    title='EDIT JUDGES - Rhythm and Rhyme'
    comp = CurrentComp.query.filter_by(id=1).first()
    judges = Judge.query.all()

    if request.method == 'POST':

        judge_a = User.query.filter_by(section="judge_a").first()
        judge_b = User.query.filter_by(section="judge_b").first()
        judge_c = User.query.filter_by(section="judge_c").first()
        judge_d = User.query.filter_by(section="judge_d").first()
        judge_e = User.query.filter_by(section="judge_e").first()

        j_a = Judge.query.filter_by(name=request.form.get("ja")).first()
        j_b = Judge.query.filter_by(name=request.form.get("jb")).first()
        j_c = Judge.query.filter_by(name=request.form.get("jc")).first()
        j_d = Judge.query.filter_by(name=request.form.get("jd")).first()
        j_e = Judge.query.filter_by(name=request.form.get("je")).first()

        judge_a.username = j_a.username
        judge_a.password = j_a.password
        comp.ja = j_a.name

        judge_b.username = j_b.username
        judge_b.password = j_b.password
        comp.jb = j_b.name

        judge_c.username = j_c.username
        judge_c.password = j_c.password
        comp.jc = j_c.name

        judge_d.username = j_d.username
        judge_d.password = j_d.password
        comp.jd = j_d.name

        judge_e.username = j_e.username
        judge_e.password = j_e.password
        comp.je = j_e.name

        db.session.commit()

        message = "Judges Updated"
        return render_template('admin/admin-response.html', title = 'Response', message=message)

    return render_template('admin/edit-judges.html', title=title, comp=comp, judges=judges)



@app.route("/edit_comp", methods=['GET', 'POST'])
def edit_comp():
    title="CREATE COMPETITION  - Rhythm and Rhyme"
    comp = CurrentComp.query.filter_by(id=1).first()
    judges = Judge.query.all()
    contenders = Entry.query.all()

    months = ["January", " February", "March", "April", " May",
    "June", "July", "August", "September", "October", "November",  "December"]

    days = [d for d in range(1, 32)]

    dead_time = comp.deadline.split(" ")[3]
    ann_time = comp.announce.split(" ")[3]

    dead_date = {"month":comp.deadline.split(" ")[0],
    "day":comp.deadline.split(" ")[1].replace(',',''),
    "year":comp.deadline.split(" ")[2],
    "hour":dead_time.split(":")[0],
    "minute":dead_time.split(":")[1],
    "second":dead_time.split(":")[2]}

    ann_date = {"month":comp.announce.split(" ")[0],
    "day":comp.announce.split(" ")[1],
    "year":comp.announce.split(" ")[2],
    "hour":ann_time.split(":")[0],
    "minute":ann_time.split(":")[1],
    "second":ann_time.split(":")[2]}


    if request.method == 'POST':
        if request.form.get("submit") == "title-btn":
            comp.title = request.form.get('title')
            comp.tag = request.form.get('tag')
            comp.round = request.form.get('round')

            db.session.commit()

        elif request.form.get("submit") == "deadline":
            d_month = request.form.get("d-month")
            d_day = request.form.get("d-day")
            d_year = request.form.get("d-year")
            d_hour = request.form.get("d-hour")
            d_minute = request.form.get("d-minute")
            d_seconds = request.form.get("d-second")

            comp.deadline = "{} {}, {} {}:{}:{} GMT+8".format(d_month, d_day, d_year, d_hour, d_minute, d_seconds)

            a_month = request.form.get("a-month")
            a_day = request.form.get("a-day")
            a_year = request.form.get("a=year")
            a_hour = request.form.get("a-hour")
            a_minute = request.form.get("a-minute")
            a_seconds = request.form.get("a-second")

            comp.announce = "{} {}, {} {}:{}:{} GMT+8".format(a_month, a_day, a_year, a_hour, a_minute, a_seconds)

            db.session.commit()

        elif request.form.get("submit") == "criteria":
            comp.crit1 = request.form.get("crit1")
            comp.crit2 = request.form.get("crit2")
            comp.crit3 = request.form.get("crit3")
            comp.per1 = request.form.get("per1")
            comp.per2 = request.form.get("per2")
            comp.per3 = request.form.get("per3")

            db.session.commit()

        message = "Competition Updated"
        return render_template('admin/admin-response.html', title = 'Response', message=message)

    return render_template('admin/comp-panel.html', title=title, comp=comp, judges=judges, contenders=contenders, months=months, days=days, ann=ann_date, dead=dead_date)


@app.route('/delete_entry', methods=['GET', 'POST'])
def delete_contender():

    if request.method == 'POST':
        name = request.form.get("delete")
        con = Entry.query.filter_by(line_name=name).first()
        backup = BackupEntry(line_name=con.line_name, link=con.link, deleted=mtime.now(), ja=con.ja, jb=con.jb, jc=con.jc, jd=con.jd, je=con.je)
        db.session.add(backup)
        db.session.delete(con)
        db.session.commit()
        db.session.rollback()

        message = "{}'s entry has been deleted!"

        return render_template('admin/admin-response.html', message=message)

    return redirect(url_for('edit_entry'))

@app.route('/edit_entry', methods=['GET'])
def edit_entry():
    title = "EDIT ENTRY"
    entries = Entry.query.all()
    if request.method == 'POST':
        name = request.form.get('delete')
        target = Entry.query.filter_by(line_name=name).first()
        return render_template('admin/delete-entry-confirm.html', target=target)
    return render_template('admin/delete-entry.html', title=title, entries=entries)

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    if request.method == "POST":
        name = request.form.get('delete')
        message = '{} has been deleted!'.format(name)
        d = Entry.query.filter_by(line_name=name).first()

        new = BackupEntry(line_name = d.line_name, link=d.link, deleted=mtime.now(), ja=d.a, jb=d.jb, jc=d.jc, jd=d.jd, je=d.je)
        db.session.add(new)

        db.session.delete(d)
        db.session.commit()
        db.session.rollback()
        return render_template('admin/edit-enry-response.html', message=message)

@app.route('/register_contender', methods=['GET', "POST"])
def register_contender():
    title = "CONTENDERS REGISTRATION - Rhythm and Rhyme"
    comp = CurrentComp.query.filter_by(id=1).first()

    if request.method == "POST":
        name = request.form.get('name')
        group = request.form.get('group')
        smule = request.form.get('smule')

        old = Contenders.query.filter_by(line_name=name).first()
        if 'file' not in request.files:
            return render_template('response.html')
        file = request.files['file']
        if file.filename == '':
            return render_template('response.html')
        if file and allowed_file(file.filename):
            filename = '{}-{}-{}.{}'.format(name, group, smule, file.filename.split('.')[-1])
            if filename and not old:
                file.save(os.path.join(cont_profile, secure_filename(filename)))

                new = Contenders(line_name=name, group=group, smule=smule, picture=filename)
                db.session.add(new)
                db.session.commit()

                info = "You are now registered for {} competition.".format("RRVSS1")
                message = "Please refer to our Comp. Coordinator and Officers for more info."
                return render_template('responses/response.html', title=title, info=info, message=message)
            else:
                info = 'You are already registered for this competition'
                message = "Please refer to our Comp. Coordinator and Officers for assistance."
                return render_template('responses/response.html', title=title, info=info, message=message)
        else:
            info = 'Invalid file!'
            message = "Please check your file."
            return render_template('responses/response.html', title=title, info=info, message=message)

    return render_template('registration/register_contender.html', title=title, comp=comp)

@app.route('/submit_entry', methods=['GET', 'POST'])
def submit_entry():
    title = "ENTRY SUBMISSION - Rhythm and Rhyme"
    comp = CurrentComp.query.filter_by(id=1).first()
    contenders = Contenders.query.all()

    if request.method == 'POST':
        registered = []
        for contender in contenders:
            registered.append(contender.line_name)

        name = request.form.get("name")
        cont = Entry.query.filter_by(line_name=name).first()
        if name in registered:
            if not cont:
                title = request.form.get("title")
                link = get_smule_link(request.form.get("link"))
                frame = ""
                submitted = mtime.now()
                ja = "0.00-0.00-0.00"
                jb = "0.00-0.00-0.00"
                jc = "0.00-0.00-0.00"
                jd = "0.00-0.00-0.00"
                je = "0.00-0.00-0.00"
                comment1 = 'comment'
                comment2 = 'comment'

                new = Entry(line_name=name, title=title, link=link, frame=frame, submitted=submitted, ja=ja, jb=jb, jc=jc, jd=jd, je=je, comment1=comment1, comment2=comment2)
                db.session.add(new)
                db.session.commit()
                info = " Your entry has been submitted!"
                message = " The result of the competition for this round will be posted soon. see info below."
                return render_template("responses/response.html", title=title, info=info, message=message)
            else:
                info = "You have already submited an entry!"
                message = "If you have not yet submitted your entry, please ask any Rhythm and Rhyme officers for assistance."
                return render_template("responses/response.html", title=title, info=info, message=message)
        else:
            info = "Submission have been blocked!"
            message = "You are not/no longer registered to participate in this competition. Please refer to any Rhythm and Rhyme officers for assistance."
            return render_template("responses/response.html", title=title, info=info, message=message)

    return render_template('registration/entry_form.html', title=title, comp=comp)




@app.route('/score_sheet', methods=['GET', 'POST'])
@login_required
def score_sheet():
    title='SCORE SHEET - Rhythm and Rhyme'
    comp = CurrentComp.query.filter_by(id=1).first()
    contenders = Entry.query.all()

    def total(text):
        x = list(text.split('-'))
        per1 = float(comp.per1[:-1]) / 100
        per2 = float(comp.per2[:-1]) / 100
        per3 = float(comp.per3[:-1]) / 100
        tot = (float(x[0]) * per1) + (float(x[1]) * per2) + (float(x[2]) * per3)
        return tot


    if request.method == "POST":
        name = request.form.get("name")
        cont = Entry.query.filter_by(line_name=name).first()

        old_score = None
        if current_user.section == 'judge_a':
            old_score = cont.ja.split("-")
        if current_user.section == "judge_b":
            old_score = cont.jb.split("-")
        if current_user.section == "judge_c":
            old_score = cont.jc.split("-")
        if current_user.section == "judge_d":
            old_score = cont.jd.split("-")
        if current_user.section == "judge_e":
            old_score = cont.je.split("-")

        return render_template("score-sheet.html", contender=cont, score=old_score, comp=comp)

    if current_user.kind == 'judge':
        all = []
        if current_user.section == "judge_a":
            for i in range(len(contenders)):
                name = contenders[i].line_name
                badge = Contenders.query.filter_by(line_name=name).first().picture
                contender = {"badge":badge, "no":i+1,"name":name, "total":total(contenders[i].ja)}
                all.append(contender)
        elif current_user.section == "judge_b":
            for c in contenders:
                name = contenders[i].line_name
                badge = Contenders.query.filter_by(line_name=name).first().picture
                contender = {"badge":badge, "no":i+1,"name":contenders[i].line_name, "total":total(contenders[i].jb)}
                all.append(contender)
        elif current_user.section == "judge_c":
            for c in contenders:
                name = contenders[i].line_name
                badge = Contenders.query.filter_by(line_name=name).first().picture
                contender = {"badge":badge, "no":i+1,"name":contenders[i].line_name, "total":total(contenders[i].jc)}
                all.append(contender)
        elif current_user.section == "judge_d":
            for c in contenders:
                name = contenders[i].line_name
                badge = Contenders.query.filter_by(line_name=name).first().picture
                contender = {"badge":badge, "no":i+1,"name":contenders[i].line_name, "total":total(contenders[i].jd)}
                all.append(contender)
        else:
            for c in contenders:
                name = contenders[i].line_name
                badge = Contenders.query.filter_by(line_name=name).first().picture
                contender = {"badge":badge, "no":i+1,"name":contenders[i].line_name, "total":total(contenders[i].je)}
                all.append(contender)

        return render_template("sheet_list.html", title=title, contenders=all, comp=comp)
    else:
        info = "You are not logged in as Judge"
        message = "Please ask any Rhythm and Rhyme officers for assistance or just log in as judge"
        return render_template('responses/response.html', title=title, info=info, message=message)


@app.route('/save_score', methods=['GET', 'POST'])
@login_required
def save_score():
    title = "SCORE SHEET - Rhythm and Rhyme"

    if request.method == "POST":
        name = request.form.get("name")
        contender = Entry.query.filter_by(line_name=name).first()

        crit1 = float(request.form.get("crit1"))
        crit2 = float(request.form.get("crit2"))
        crit3 = float(request.form.get("crit3"))
        score = "{}-{}-{}".format(crit1, crit2, crit3)

        if current_user.section == "judge_a":
            contender.ja = score
            db.session.commit()
            return redirect(url_for("score_sheet"))

        if current_user.section == "judge_b":
            contender.jb = score
            db.session.commit()
            return redirect(url_for("score_sheet"))

        if current_user.section == "judge_c":
            contender.jc = score
            db.session.commit()
            return redirect(url_for("score_sheet"))

        if current_user.section == "judge_d":
            contender.jd = score
            db.session.commit()
            return redirect(url_for("score_sheet"))

        if current_user.section == "judge_e":
            contender.je = score
            db.session.commit()
            return redirect(url_for("score_sheet"))


    if current_user.kind == "judge":
        return render_template("scoresheet.html", title=title, contender=contender)
    else:
        info = " You are not registered as judge"
        message = " Please ask any Rhythm and Rhyme officers for assistance"
        return render_template('responses/response.html', title=title, info=info, message=message)


@app.route("/result", methods=['GET', 'POST'])
def result():
    title = "RESULT - Rhythm and Rhyme"
    entries = Entry.query.all()
    comp = CurrentComp.query.filter_by(id=1).first()
    per1 = float(comp.per1.replace("%", "")) / 100
    per2 = float(comp.per2.replace("%", "")) / 100
    per3 = float(comp.per3.replace("%", "")) / 100

    contenders = []
    for con in entries:
        badge = Contenders.query.filter_by(line_name=con.line_name).first().picture
        ja = (float(con.ja.split('-')[0]) * per1) + (float(con.ja.split('-')[1]) * per2) + (float(con.ja.split('-')[2]) * per3)
        jb = (float(con.jb.split('-')[0]) * per1) + (float(con.jb.split('-')[1]) * per2) + (float(con.jb.split('-')[2]) * per3)
        jc = (float(con.jc.split('-')[0]) * per1) + (float(con.jc.split('-')[1]) * per2) + (float(con.jc.split('-')[2]) * per3)
        jd = (float(con.jd.split('-')[0]) * per1) + (float(con.jd.split('-')[1]) * per2) + (float(con.jd.split('-')[2]) * per3)
        je = (float(con.je.split('-')[0]) * per1) + (float(con.je.split('-')[1]) * per2) + (float(con.je.split('-')[2]) * per3)
        total = (ja + jb + jc + jd + je) / 5
        contender = Result(badge, con.line_name, ja, jb, jc, jd, je, total)
        contenders.append(contender)

    for i in range(len(contenders)):
        all_total = []
        for all in contenders:
            all_total.append(all.total)

        contenders[i].rank = rank(contenders[i].total, all_total)

    if request.method == "POST":
        name = request.form.get("get")
        con = Entry.query.filter_by(line_name=name).first()
        info = scoreinfo(name, per1, per2, per3, con.ja, con.jb, con.jc, con.jd, con.je)

        return render_template("score-info.html", title=title, score=info)

    return render_template("result.html", title=title, contenders=contenders)

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    title = 'GALLERY - Rhythmand Rhyme'

    if request.method == 'POST':
        cat = request.form.get('cathegory')
        album = Picture.query.filtar_by(category=cat).all()

        return render_template('album.html', title=cat, album=album)

    return render_template('gallery.html', title=title)

@app.route('/upload_picture', methods=['POST', 'GET'])
def upload_picture():
    title = 'MANAGE PICTURE - Rhythm and Rhyme'
    categories = ['Meet Ups', 'Achievements', 'Recognitions', 'Activities']
    if request.method == 'POST':
        cat = request.form.get('category')
        description = request.form.get('desc')
        uptime = mtime.now()

        file = request.files['file']
        if file.filename == "":
            message = "Problem with file"
            return render_template('admin/admin-response.tml', message=message)
        if file and allowed_file(file.filename):
            file_name = "{}-{}.{}".format(cat, uptime.split(':')[0], file.filename.split('.')[-1])
            file_name2 = file_name.replace(" ", "_")
            filename = file_name2.replace(",", "")
            if filename:
                file.save(os.path.join(gallery_dir, secure_filename(filename)))

                new = Picture(picture=filename, description=description, category=cat)
                db.session.add(new)
                db.session.commit()
                message = "Image uplaoded"
                return render_template('admin/admin-response.html', title=title, message=message)

    return render_template('admin/upload-picture.html', title=title, categories=categories)

@app.route('/recognition_gallery', methods=['GET'])
def recognition_gallery():
    title=" RECOGNITION - Rhythm and Rhyme"
    recognitions = Picture.query.filter_by(category="Recognitions").all()
    return render_template('recognition-gallery.html', title=title, recognitions=recognitions)
