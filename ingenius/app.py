

from flask import Flask,request,render_template, redirect,url_for,jsonify,make_response
app=Flask(__name__)
from flask_pymongo import PyMongo
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/ras"
mongo = PyMongo(app)

@app.route("/",methods=['POST'])
def retrieve():	
	name=request.form['nm']
	age=request.form['age']
	email=request.form['email']
	interest=request.form['interest']
	password=request.form['password']

	indb=mongo.db.ras.find(
		{'email' : email
		})
	for x in indb:
		if(x["email"]==request.form['email']):
			return "user aldready exists"
	mongo.db.ras.insert_one({
		'name':name,'age':age,'email':email,'interest':interest,'password':password,'level':1,
		})
	return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
	email=request.form['email']
	password=request.form['password']
	email1=mongo.db.ras.find({
		'email':email
		})
	
	password1=mongo.db.ras.find({
		'password':password
		
		})
	for value in email1:
		if (value["email"]==request.form['email']):
			for value1 in password1:
				if(value1["password"]==request.form['password']):
					return render_template('quiz.html')



		
	return "The password or Email you entered is incorrect"


@app.route('/quizinfo',methods=['POST'])
def fun():
	global question,ans,lev,final
	email=request.form['email']
	ind=mongo.db.ras.find({
		'email':email
		})
	for val in ind:
		if(val['email']==email):
			mail={
			'email':request.form['email']
			}
			(jsonify(mail),200)
			ind=mongo.db.ras.find({
				'email':mail['email']
				})
			#return ind
			for va in ind:
				name=va['name']
				level=va['level']
			final={
				'name':name,
				'email':mail['email'],
				'level':level
			}
			(jsonify(final),200)
			#mongo.db.quiz.insert({#this part is not required as aldready questions are present on database used for sample
				#'level':'3',
				#'question':'what is the letter after b',
				#'answer':'c'
				#})
			#return (final['level'])
			
			level1=mongo.db.quiz.find({

				'level':str(final['level'])

				})
			for y in level1:
			   	question=y['question']
			   	ans=y['answer']
			   	lev=y['level']
			return render_template('answer.html',ques=question,lev1=lev)
	return "mail not registered"	

@app.route('/answer',methods=['POST'])
def ret():
	global ans,lev
	answer=request.form['answer']
	if(answer==ans):
		mongo.db.ras.update({
			'email':final['email']
			},
			{
			"$inc":{
			'level':1
			}
			}
			)
		t=mongo.db.ras.find({
			'email':final['email']
			})
		global question
		for f in t:
			lev=f['level']
			if(lev==6):
				return "you have successfully completed the quiz"
				break
			x=mongo.db.quiz.find({
			'level':str(lev)
			})
			for a in x:
				lev=a['level']
				question=a['question']
				ans=a['answer']

			return render_template('answer.html',ques=question,lev1=lev)
	return "wrong answer!!click back and try again"

if __name__ == "__main__":
    app.run(debug = True)

 
