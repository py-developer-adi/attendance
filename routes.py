'''PyCODE | @_py.code'''

# ? Importing Libraries
from flask import Blueprint, render_template, redirect, flash, request
from extensions import *
from uuid import uuid4

# ! INITIALIZING ROUTER
router = Blueprint('router', __name__)

# | Logger Route
@logger.user_loader
def load_user(user):
    return User.query.get(user)

# & Base Route
@router.route('/')
def base():
    if current_user.is_authenticated:
        return redirect('/dash')
    else:
        return redirect('/login')
    
# & Login Route
@router.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash("Email not found! Try sign-in Instead.", "error")
            return redirect('/login')
        
        if not check_password_hash(user.password, password):
            flash("Invalid Password", "error")
            return redirect('/login')
        
        login_user(user)
        flash("Welcome Back", "success")
        return redirect('/dash')
    
# & Sign-in Route
@router.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('auth.html')
    else:
        id = str(uuid4())
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash("Email already exists! Try login instead", "error")
            return redirect('/signin')
        
        new_user = User(
            id=id, username=username, email=email,
            password=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash("Welcome!", "success")
        return redirect('/dash')
    
# & Logout Route
@router.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

# & Dash Route
@router.route('/dash')
def dash():
    if current_user.is_authenticated:
        # Get current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        today = date.today()
        
        all_frame = Attendance.query.filter_by(attender=current_user.username).all()

        monthly_frame = Attendance.query.filter_by(attender=current_user.username)\
            .filter(extract('month', Attendance.date) == current_month)\
            .filter(extract('year', Attendance.date) == current_year)\
            .all()
            
        # Weekly filter for SQLite
        weekly_frame = Attendance.query.filter_by(attender=current_user.username)\
            .filter(func.strftime('%W', Attendance.date) == func.strftime('%W', 'now'))\
            .filter(func.strftime('%Y', Attendance.date) == func.strftime('%Y', 'now'))\
            .all()
            
        daily_frame = Attendance.query.filter_by(attender=current_user.username)\
            .filter(func.date(Attendance.date) == today)\
            .all()
        
        attendees = Attendee.query.filter_by(manager=current_user.username).all()
        return render_template('dash.html', 
            attendees=attendees,
            all_frame=all_frame,
            monthly_frame=monthly_frame,
            weekly_frame=weekly_frame,
            daily_frame=daily_frame
        )
    return redirect('/login')

# & New-Attendee Route
@router.route('/new-attendee', methods=['POST'])
def new_attendee():
    name = request.form.get('name')
    role = request.form.get('role')
    email = request.form.get('email', "")
    mobile = request.form.get('mobile', "")
    
    if email != "":
        if Attendee.query.filter_by(email=email).first():
            flash("Email already registered with another attendee", 'error')
            return redirect('/dash')
        
    if mobile != "":
        if Attendee.query.filter_by(mobile=mobile).first():
            flash("Mobile is already regsiter with another attendee", "error")
            return redirect('/dash')
        
    new_attendee = Attendee(
        id=str(uuid4()),
        name=name,
        role=role,
        manager=current_user.username,
        email=email,
        mobile=mobile
    )
    
    db.session.add(new_attendee)
    db.session.commit()
    
    flash("New Attendee added successfully", "success")
    return redirect('/dash')

# & Edit Attendee Route
@router.route('/edit-attendee', methods=['POST'])
def edit_attendee():
    id = request.form.get('id')
    name = request.form.get('name')
    role = request.form.get('role')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    
    attendee = Attendee.query.filter_by(id=id).first()
    
    if not attendee:
        flash("Attendee not found", "error")
        return redirect('/dash')
    
    if Attendee.query.filter_by(email=email).first() and email != "" and attendee.email != email:
        flash("Email already registered with another attendee.", "error")
        return redirect('/dash')
    
    if Attendee.query.filter_by(mobile=mobile).first() and mobile != "" and attendee.mobile != mobile:
        flash("Mobile Already registered with another attendee", ",error")
        return redirect('/dash')
    
    attendee.name = name
    attendee.role = role
    attendee.email = email if email else ""
    attendee.mobile = mobile if mobile else ""
    
    db.session.commit()
    flash("Attendee edited successfully", "success")
    return redirect('/dash')

# & Help Route
@router.route('/help', methods=['POST'])
def help_():
    subject = request.form.get("subject")
    help_c = request.form.get("help")
    
    new_help = Help(
        id=str(uuid4()),
        subject=subject, help=help_c,
        email=current_user.email
    )
    
    db.session.add(new_help)
    db.session.commit()
    
    flash("Your query is submitted!", "success")
    return redirect('/dash')

# & Mark Attendance Route
@router.route('/mark/<id>')
def mark(id):
    attendee = Attendee.query.filter_by(id=id).first()
    attendance = Attendance.query.filter_by(date=date.today()).all()
    
    if attendee:
        if attendance:
            for att in attendance:
                if att.attendee == attendee.id:
                    flash("Attendance already marked", "warning")
                    return redirect('/dash')
                
        new_attendace = Attendance(
            id=str(uuid4()),
            attendee=attendee.id,
            attender=current_user.username,
            date=datetime.utcnow().date(),
            status="Present"
        )
        
        db.session.add(new_attendace)
        db.session.commit()
        
        flash("Attendace Marked", "success")
        return redirect('/dash')
        
    flash("Attendee not found!", "danger")
    return redirect('/dash')

# | Socket Route for Search-for-Attendee
@socket.on('sfa')
def sfa(name):
    attendee = Attendee.query.filter_by(id=name).first()
    
    if not attendee:
        socket.emit('sfa-out', [
            "Attendee Not Found!",
            "", "", "", ""
        ])
        return
        
    socket.emit('sfa-out', [
        attendee.id,
        attendee.name,
        attendee.role,
        attendee.email,
        attendee.mobile
    ])
    
# | Socket Route for All-Attendees
@socket.on('aa')
def aa(name):
    attendees = Attendee.query.filter(
        Attendee.name.ilike(f"%{name}%")
    ).all()
    
    if not attendees:
        socket.emit(["No Attendees Found!"])
        return
    
    atl = []
    for attendee in attendees:
        atl.append([
            attendee.id,
            attendee.name,
            attendee.role
        ])
    
    socket.emit('aa-out', atl)
    
# | Socket Route for Delete-Attendee
@socket.on('del')
def del_att(id):
    attendee = Attendee.query.filter_by(id=id).first()
    
    if attendee:
        db.session.delete(attendee)
        db.session.commit()
        
# | Socket Route for Reset-Data
@socket.on('reset')
def reset(boolean):
    if not boolean:
        return redirect('/dash')
    
    else:
        attendees = Attendee.query.filter_by(manager=current_user.username).all()
        attendances = Attendance.query.filter_by(attender=current_user.username).all()
        
        for attendee in attendees:
            db.session.delete(attendee)
            db.session.commit()
            
        for attendance in attendances:
            db.session.delete(attendance)
            db.session.commit()
            
        flash("All data deleted successfully", "warning")
        return redirect('/dash')