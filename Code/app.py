from flask import Flask, render_template, request,flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key="secret@1234"
app.config['UPLOAD_FOLDER'] = 'static/audios'

db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class usermodel(db.Model):
    
    username=db.Column(db.String,primary_key=True,nullable=False)
    password=db.Column(db.String,nullable=False)

class influencer(db.Model):
    __tablename__="influencer"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    emailid=db.Column(db.String,nullable=False)
    fullname=db.Column(db.String,nullable=False)
    username=db.Column(db.String,nullable=False)
    pasword=db.Column(db.String,nullable=False)
    platform=db.Column(db.String)
    niche=db.Column(db.String,nullable=False)

class sponsor(UserMixin,db.Model):
    __tablename__="sponsor"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    emailid=db.Column(db.String,nullable=False)
    fullname=db.Column(db.String,nullable=False)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    industry=db.Column(db.String,nullable=False)

    def __repr__(self) -> str:
        return '<User %r>' % self.fName

class campaign(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    title=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    niche=db.Column(db.String,nullable=False)
    date=db.Column(db.Integer,nullable=False)
    sponsor_username = db.Column(db.String, nullable=False)
    influencer_username = db.Column(db.String)
    Status= db.Column(db.String)
    
    def __repr__(self):
        return f"<Campaign {self.title}>"
    

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return sponsor.query.get(int(user_id))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pasword = request.form.get("password")
        


        user = influencer.query.filter(influencer.username==username).first()
        
        if user and pasword==user.pasword:
            
            return redirect(url_for('influencer_dashboard', username=user.username))
        else:
            user1 = sponsor.query.filter(sponsor.username==username).first()
        
            if user1 and pasword==user1.password:
                login_user(user1)
            
                return redirect(url_for('profile1', username=user1.username))
        return "Login failed"        
    return render_template("login.html")

@app.route("/profile1/<username>",methods=["GET","POST"])
def profile1(username):
    user1 = sponsor.query.filter(sponsor.username==username).first()
    if user1:
        industry_value = user1.industry
    return render_template("sponsorprofile.html",Username=username,Industry=industry_value,)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route("/admin",methods=["GET","POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        pasword = request.form.get("password")
        


        
        if username=="admin@123" and pasword=="123":
            return redirect(url_for('admin_dashboard'))
        else:
            return "Login failed"
    return render_template("adminlogin.html")



@app.route("/influencer_register",methods=["GET","POST"])
def influencer_registration():

    if request.method == "POST":
        emailid= request.form.get("emailid")
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        pasword = request.form.get("password")
        #platform = request.form.get("platform")
        niche = request.form.get("niche")
        user=influencer.query.filter(influencer.username==username).first()
        
        if not user:
            print(user)
            new_user=influencer(emailid=emailid,fullname=fullname,username=username,pasword=pasword,niche=niche)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",msg="")
        else:
            return render_template("influencerreg.html",msg="User is already exists!!")
        
    return render_template("influencerreg.html",msg="")


@app.route("/sponsor_registration",methods=["GET","POST"])
def sponsor_registration():
    if request.method == "POST":
        emailid = request.form.get("emailid")
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        password = request.form.get("password")
        industry = request.form.get("industry")
        user=sponsor.query.filter(sponsor.username==username).first()
        if not user:
            new_user=sponsor(emailid=emailid,fullname=fullname,username=username,password=password,industry=industry)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",msg="")
        else:
            return render_template("sponsorreg.html",msg="User already exists!!")
        
    return render_template("sponsorreg.html",msg="")

@app.route("/add_campaign", methods=["GET", "POST"])
def add_campaign():
    if request.method == "POST":
        user_id = current_user.get_id()
        sponsor1=sponsor.query.filter(sponsor.id==user_id).first()
        sponsor_username=sponsor1.username
        title = request.form.get("title")
        description = request.form.get("description")
        niche = request.form.get("niche")
        #date = datetime.strptime(request.form.get("date"), '%d-%m-%Y')
        date = datetime.strptime(request.form.get("date"), '%Y-%m-%d')

        #sponsor_username = request.form.get("sponsor_username")  # Assume this is passed in the form

        new_campaign = campaign(title=title, description=description, niche=niche, date=date,sponsor_username=sponsor_username,Status="Pending",influencer_username="None")
        db.session.add(new_campaign)
        db.session.commit()
        return("Okay")
        #return redirect(url_for('sponsor_dashboard', username=sponsor_username))
    
    return render_template("sponsorcampaignsadd.html")

@app.route("/sponsor_dashboard")
def sponsor_dashboard():
    user_id = current_user.get_id()
    sponsor1=sponsor.query.filter(sponsor.id==user_id).first()
    sponsor_username=sponsor1.username
    campaigns = campaign.query.filter(campaign.sponsor_username==sponsor_username).all()
    sponsor_id = request.args.get('username')
    #campaigns = campaign.query.filter_by(campaign.username==username).all()
    return render_template("sponsorcampaigns.html",campaigns=campaigns)
@app.route('/delete_campaign/<name>', methods=['POST'])
def delete_campaign(name):
    campaigns = campaign.query.filter(campaign.title==name).first()

    db.session.delete(campaigns)
    db.session.commit()    
    return redirect(url_for('sponsor_dashboard'))

@app.route('/delete_campaign1/<name>', methods=['POST'])
def delete_campaign1(name):
    campaigns = campaign.query.filter(campaign.title==name).first()

    db.session.delete(campaigns)
    db.session.commit()    
    return redirect(url_for('admin_dashboard'))


@app.route('/edit_campaign/<int:c_id>', methods = ['GET', 'POST'])
def edit_campaign(c_id):
    campaigns = campaign.query.filter(campaign.id==c_id).first()

    if request.method == 'POST':
        campaigns.title = request.form.get('campaign_name')
        campaigns.description=request.form.get('campaign_description')
        db.session.commit()
        
        return redirect(url_for('sponsor_dashboard'))
    
    return render_template('edit.html', campaigns=campaigns)

@app.route('/edit_campaign1/<int:c_id>', methods = ['GET', 'POST'])
def edit_campaign1(c_id):
    campaigns = campaign.query.filter(campaign.id==c_id).first()

    if request.method == 'POST':
        campaigns.title = request.form.get('campaign_name')
        campaigns.description=request.form.get('campaign_description')
        db.session.commit()
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('edit.html', campaigns=campaigns)
@app.route('/search_results1')
def search_results1():
    search_query = request.args.get('search_keywords')

    if search_query:
        campaigns= campaign.query.filter(campaign.title.ilike(f'%{search_query}%')).all()
        print(campaigns)
    
        return render_template('search_results1.html',campaigns=campaigns)

@app.route('/search_results')
def search_results():
    search_query = request.args.get('search_keywords')

    if search_query:
        influencers= influencer.query.filter(influencer.username.ilike(f'%{search_query}%')).all()
    
        return render_template('search_results.html',influencers=influencers)


@app.route("/influencer_dashboard")
def influencer_dashboard():
    username = request.args.get('username')
    campaigns = campaign.query.filter(campaign.influencer_username=="None").all()

    
    return render_template("influencercampaigns.html",campaigns=campaigns,username=username)

@app.route("/campaigns")
def campaigns():
    username = request.args.get('username')
    campaigns = campaign.query.filter(campaign.influencer_username==username).all()

    
    return render_template("campaigns.html",campaigns=campaigns,username=username)


@app.route("/admin_dashboard")
def admin_dashboard():
    campaigns = campaign.query.all()
    influencers = influencer.query.all()
    campaigns1= campaign.query.filter(campaign.Status=="Acept").all()
    return render_template("admindashboard.html",campaigns=campaigns,influencers=influencers,campaigns1=campaigns1)
@app.route("/SPrequest")
def SPrequest():
    user_id = current_user.get_id()
    user=sponsor.query.filter(sponsor.id==user_id).first()
    campaigns = campaign.query.filter(campaign.sponsor_username==user.username,campaign.Status=="Pending").all()
    campaigns1= campaign.query.filter(campaign.sponsor_username==user.username,campaign.Status=="Acept").all()
    campaigns2= campaign.query.filter(campaign.sponsor_username==user.username,campaign.Status=="Reject").all()
    username = request.args.get('username')
    
    return render_template("sponsorrequest.html",campaigns=campaigns,campaigns1=campaigns1,campaigns2=campaigns2)


@app.route('/Acept/<int:id>',methods=['GET'])
def Acept(id):
    campaigns=campaign.query.get(id)
    campaigns.Status="Acept"
    db.session.commit()
    return redirect(url_for('SPrequest'))
@app.route('/profile/<username>',methods=['GET'])
def profile(username):
    user=influencer.query.filter(influencer.username==username).first()
    return render_template('influencerprofile.html',user=user)    

@app.route('/Request/<int:id>/<username>',methods=['GET'])
def Request(id,username):
    campaigns=campaign.query.get(id)
    campaigns.influencer_username=username
    db.session.commit()
    return redirect(url_for('influencer_dashboard', username=username))
    



@app.route('/Reject/<int:id>',methods=['GET'])
def Reject(id):
    requests=campaign.query.get(id)
    requests.Status="Reject"
    db.session.commit()
    return redirect(url_for('SPrequest'))

if __name__=="__main__":
    app.run(debug=True)