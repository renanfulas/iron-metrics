from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import plotly.express as px
import plotly.utils
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iron_metrics.db'
app.config['SECRET_KEY'] = 'chave-secreta-iron-123'
db = SQLAlchemy(app)

# --- MODELOS ---

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    assessments = db.relationship('Assessment', backref='student', lazy=True, cascade="all, delete-orphan")
    perimetrias = db.relationship('Perimetria', backref='student', lazy=True, cascade="all, delete-orphan")

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    weight = db.Column(db.Float)
    body_fat = db.Column(db.Float)
    lean_mass = db.Column(db.Float)
    fat_mass = db.Column(db.Float)
    # Dobras cutâneas
    triceps = db.Column(db.Float, default=0.0)
    subscapular = db.Column(db.Float, default=0.0)
    chest = db.Column(db.Float, default=0.0)
    axillary = db.Column(db.Float, default=0.0)
    suprailiac = db.Column(db.Float, default=0.0)
    abdominal = db.Column(db.Float, default=0.0)
    thigh = db.Column(db.Float, default=0.0)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

class Perimetria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    height = db.Column(db.Float, default=0.0)
    weight = db.Column(db.Float, default=0.0)
    arm = db.Column(db.Float, default=0.0)
    forearm = db.Column(db.Float, default=0.0)
    chest = db.Column(db.Float, default=0.0)
    waist = db.Column(db.Float, default=0.0)
    abdomen = db.Column(db.Float, default=0.0)
    hip = db.Column(db.Float, default=0.0)
    thigh = db.Column(db.Float, default=0.0)
    calf = db.Column(db.Float, default=0.0)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == 'admin': 
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# --- ROTAS PRINCIPAIS ---

@app.route('/')
def dashboard():
    if not session.get('logged_in'): return redirect(url_for('login'))
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    if not session.get('logged_in'): return redirect(url_for('login'))
    name = request.form.get('name')
    if name:
        db.session.add(Student(name=name))
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/student/<int:id>')
def student_detail(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    student = Student.query.get_or_404(id)
    assessments = Assessment.query.filter_by(student_id=id).order_by(Assessment.date.desc()).all()
    
    graph_line_json = "{}"
    graph_pie_json = "{}"
    
    if assessments:
        # Gráfico de Evolução (Linha) - Ordem cronológica (antigo para novo)
        asc_data = sorted(assessments, key=lambda x: x.date)
        fig_l = px.line(
            x=[a.date.strftime("%d/%m") for a in asc_data], 
            y=[a.body_fat for a in asc_data], 
            markers=True, 
            template='plotly_dark',
            title="Evolução % Gordura"
        )
        fig_l.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=20, l=20, r=20))
        graph_line_json = json.dumps(fig_l, cls=plotly.utils.PlotlyJSONEncoder)

        # Gráfico de Composição Atual (Pizza)
        latest = assessments[0]
        fig_p = px.pie(
            names=['Massa Magra', 'Massa Gorda'], 
            values=[latest.lean_mass, latest.fat_mass],
            color_discrete_sequence=['#10b981', '#ef4444'], 
            template='plotly_dark'
        )
        fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=20, r=20), showlegend=True)
        graph_pie_json = json.dumps(fig_p, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('student.html', student=student, assessments=assessments, 
                           graphLineJSON=graph_line_json, graphPieJSON=graph_pie_json)

@app.route('/add_assessment/<int:student_id>', methods=['POST'])
def add_assessment(student_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    w_val = request.form.get('weight')
    if not w_val or float(w_val) <= 0:
        return redirect(url_for('student_detail', id=student_id))

    # Trava Anti-Duplicidade (5 segundos)
    last = Assessment.query.filter_by(student_id=student_id).order_by(Assessment.date.desc()).first()
    if last and (datetime.now() - last.date).total_seconds() < 5:
        return redirect(url_for('student_detail', id=student_id))

    try:
        w = float(w_val)
        # Coleta das dobras (nomes em inglês conforme o banco)
        folds_keys = ['triceps', 'subscapular', 'chest', 'axillary', 'suprailiac', 'abdominal', 'thigh']
        folds_data = {k: float(request.form.get(k) or 0) for k in folds_keys}
        
        total_folds = sum(folds_data.values())
        bf = total_folds * 0.15 if total_folds > 0 else 0
        fat_m = (bf / 100) * w
        lean_m = w - fat_m

        new_a = Assessment(
            weight=round(w, 2), 
            body_fat=round(bf, 2),
            fat_mass=round(fat_m, 2), 
            lean_mass=round(lean_m, 2),
            **folds_data,
            student_id=student_id
        )
        db.session.add(new_a)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar avaliação: {e}")

    return redirect(url_for('student_detail', id=student_id))

@app.route('/student/<int:id>/perimetria')
def perimetria_detail(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    history = Perimetria.query.filter_by(student_id=id).order_by(Perimetria.date.desc()).all()
    return render_template('perimetria.html', student=student, history=history)

@app.route('/add_perimetria/<int:student_id>', methods=['POST'])
def add_perimetria(student_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    f = request.form
    try:
        new_p = Perimetria(
            height=float(f.get('height') or 0),
            weight=float(f.get('weight') or 0),
            arm=float(f.get('arm') or 0),
            forearm=float(f.get('forearm') or 0),
            chest=float(f.get('chest') or 0),
            waist=float(f.get('waist') or 0),
            abdomen=float(f.get('abdomen') or 0),
            hip=float(f.get('hip') or 0),
            thigh=float(f.get('thigh') or 0),
            calf=float(f.get('calf') or 0),
            student_id=student_id
        )
        db.session.add(new_p)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro perimetria: {e}")
        
    return redirect(url_for('perimetria_detail', id=student_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)