import sys
import subprocess
import threading
import random
import os                         
from fpdf import FPDF              

from flask import (
    Flask, render_template, request, redirect, url_for, session,
    jsonify, send_from_directory, flash
)
from bidi.algorithm import get_display
import arabic_reshaper

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

# ─── Monkey-patch CVZone’s open → UTF-8 ───
import builtins, cvzone.ClassificationModule as _cm
_open_orig = builtins.open
def _open_utf8(path, mode='r', *a, **kw):
    kw.setdefault('encoding', 'utf-8')
    return _open_orig(path, mode, *a, **kw)
_cm.open = _open_utf8
# ──────────────────────────────────────────

# ═══ Flask setup ═══
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# ─── EMAIL/OTP CONFIGURATION ───
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='amm4r321123@gmail.com',
    MAIL_PASSWORD='furygshxcehmmnik',
    MAIL_DEFAULT_SENDER='amm4r321123@gmail.com'
)
mail = Mail(app)

# ─── DB CONFIG ───
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tawasol.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/static/<path:filename>')
def static_proxy(filename):
    return send_from_directory('static', filename)

# ═══ MODELS for database ═══
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(255), nullable=False, server_default='12345')

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)
    ts = db.Column(db.DateTime, default=db.func.now())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    patient = db.relationship('Patient', back_populates='conversations')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    conversations = db.relationship('Conversation',
                                    back_populates='patient',
                                    cascade='all, delete-orphan',
                                    lazy=True)

# ═══ AUTH HELPERS ═══
def logged_in(): return 'user_id' in session
def admin_required(): return logged_in() and User.query.get(session['user_id']).role == 'admin'

# ═══ GENERAL PAGES ═══
@app.route('/')
def home(): return render_template('home.html')

# ---------- LOGIN / OTP ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    err = None
    if request.method == 'POST':
        u = User.query.filter_by(email=request.form['email']).first()
        if u and check_password_hash(u.password, request.form['password']):
            otp = f"{random.randint(1000,9999):04d}"
            session['otp'] = otp
            session['user_id_pending'] = u.id
            mail.send(Message('رمز التحقق', recipients=[u.email],
                              body=f'رمز التحقق الخاص بك هو: {otp}'))
            return redirect(url_for('verify_otp'))
        err = '⚠️ البريد الإلكتروني أو كلمة المرور غير صحيحة'
    return render_template('login.html', error_message=err)

@app.route('/verify_otp', methods=['GET','POST'])
def verify_otp():
    if request.method == 'POST':
        if request.form.get('otp') == session.get('otp'):
            session['user_id'] = session.pop('user_id_pending')
            session.pop('otp', None)
            role = User.query.get(session['user_id']).role
            return redirect(url_for('dashboard' if role=='admin' else 'employee_dashboard'))
        flash("الرمز المدخل غير صحيح، الرجاء إعادة المحاولة", "danger")
    return render_template('otp.html')

@app.route('/dashboard')
def dashboard():
    if not admin_required(): return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/employee_dashboard')
def employee_dashboard(): return render_template('employee_dashboard.html')

# ---------- EMPLOYEE CRUD ----------
@app.route('/add_employee', methods=['GET','POST'])
def add_employee():
    if request.method == 'POST':
        data = {k: request.form.get(k) for k in ('full_name','email','phone','role','password','gender')}
        if not all(data.values()): return "All fields required", 400
        if User.query.filter_by(email=data['email']).first(): return "User exists", 409
        db.session.add(User(
            full_name=data['full_name'], email=data['email'],
            phone=data['phone'], role=data['role'], gender=data['gender'],
            password=generate_password_hash(data['password'])
        ))
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_employee.html')

@app.route('/users')
def list_users():
    if not logged_in(): return redirect(url_for('login'))
    return render_template('users.html', users=User.query.all())

@app.post('/delete_user/<int:user_id>')
def delete_user(user_id):
    if not logged_in(): return redirect(url_for('login'))
    u = User.query.get(user_id)
    if u: db.session.delete(u); db.session.commit(); flash("User deleted!", "success")
    else: flash("Not found", "danger")
    return redirect(url_for('list_users'))

@app.route('/edit_user/<int:user_id>', methods=['GET','POST'])
def edit_user(user_id):
    u = User.query.get_or_404(user_id)
    if request.method == 'POST':
        for fld in ('full_name','email','phone','role','gender'):
            setattr(u, fld, request.form[fld])
        if pw := request.form.get('password'):
            u.password = generate_password_hash(pw)
        db.session.commit(); flash("تم التعديل!", "success")
        return redirect(url_for('list_users'))
    return render_template('edit_user.html', user=u)

@app.route('/settings')
def settings():
    if not logged_in(): return redirect(url_for('login'))
    return render_template('settings.html')

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('login'))

# ---------- PATIENT PAGES ----------
@app.route('/individuals_list')
def individuals_list():
    return render_template('individuals_list.html', patients=Patient.query.all())

@app.route('/patient_information/<int:patient_id>')
def patient_information(patient_id):
    return render_template('patient_information.html',
                           patient=Patient.query.get_or_404(patient_id))

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    if not logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        idn = request.form['id_number']
        patient = Patient.query.filter_by(id_number=idn).first()
        if not patient:
            flash("لم نعثر على المريض", "danger")
            return redirect(url_for('patient'))

        # store every recognised word
        for w in [w.strip() for w in request.form.get('log','').split('|') if w.strip()]:
            db.session.add(Conversation(text=w, patient_id=patient.id))
        db.session.commit()
        flash("تمت إضافة المحادثة!", "success")
        return redirect(url_for('patient_information', patient_id=patient.id))

    return render_template('patient.html')

@app.route('/add_patient', methods=['GET','POST'])
def add_patient():
    if not logged_in(): return redirect(url_for('login'))
    if request.method == 'POST':
        p = Patient(full_name=request.form['full_name'],
                    email=request.form['email'],
                    phone=request.form['phone'],
                    id_number=request.form['id_number'],
                    gender=request.form['gender'])
        db.session.add(p); db.session.commit()

        for w in [w.strip() for w in request.form.get('log','').split('|') if w.strip()]:
            db.session.add(Conversation(text=w, patient_id=p.id))
        db.session.commit()
        return redirect(url_for('employee_dashboard'))
    return render_template('add_patient.html')

# ---------- PDF EXPORT (NEW) ----------
@app.route('/patient_pdf/<int:pid>')
def patient_pdf(pid):
    patient = Patient.query.get_or_404(pid)
    rows = (Conversation.query.filter_by(patient_id=pid)
                             .order_by(Conversation.ts).all())

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_path = os.path.join(app.root_path, 'static', 'font', 'NotoNaskhArabic-Regular.ttf')
    pdf.add_font('Naskh', '', font_path, uni=True)
    pdf.set_font('Naskh', size=16)
    pdf.cell(0, 10,
             f"المريض: {patient.full_name}   (رقم الهوية: {patient.id_number})",
             ln=1, align='R')
    pdf.ln(5)
    pdf.set_font('Naskh', size=14)

    ts_col_w = 55
    text_col_w = pdf.w - pdf.l_margin - pdf.r_margin - ts_col_w

    # chronological order
    rows = sorted(rows, key=lambda r: r.ts)

    for r in rows:
        pdf.cell(ts_col_w, 10, r.ts.strftime("%Y-%m-%d %H:%M:%S"), align="L")

        # Arabic text cell (RTL after reshaping + bidi)
        shaped = arabic_reshaper.reshape(r.text)
        rtl = get_display(shaped)
        pdf.multi_cell(text_col_w, 10, rtl, align="R")

    tmp_dir = os.path.join(app.root_path, 'static', 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    fname = f"patient_{pid}_transcript.pdf"
    pdf.output(os.path.join(tmp_dir, fname))
    return send_from_directory(tmp_dir, fname, as_attachment=True)

# ---------- TRANSLATOR & LABEL POLLING ----------
@app.route('/translator')
def translator(): return render_template('translator.html')

@app.route('/translation_error')
def translation_error(): return render_template('translation_error.html')

LABELS = ["دق عليا","شكرا","ت","عضلة","شاش","السلام عليكم","وين","طبيب",
          "صيدلي","تعب","موعد","رجال","ولادة","كذاب","ممرضة","دورة مياه",
          "وفاة","طفل","مدير","بلعوم","جهاز تنفسي","أ","ب","د","ح","ج","خ",
          "ر","ش","س","ذ","ز","ث","التهاب"]
last_label = ""

def _reader_thread(proc):
    global last_label
    for raw in proc.stdout:
        line = raw.strip()
        if line in LABELS:
            last_label = line

@app.post('/run_test')
def run_test():
    proc = subprocess.Popen([sys.executable, '-u', 'test1.py'],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding='utf-8', errors='ignore', bufsize=1)
    threading.Thread(target=_reader_thread, args=(proc,), daemon=True).start()
    return jsonify({"started": True})

@app.get('/current_label')
def current_label():
    return jsonify({"label": last_label})

# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
