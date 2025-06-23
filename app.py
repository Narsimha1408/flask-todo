from datetime import timezone, datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

# configuring DB
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todoapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

#defining schema

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"





@app.route("/", methods=["POST", "GET"])
def renderPage():
    if request.method == "POST":
    #accessing the form elements
        title = request.form.get("title")

        description =request.form.get("description")
        todo = Todo(title=title, description=description)

        #to add and commit the changes to db
        db.session.add(todo)
        db.session.commit()

    #to list all the rows of db
    all_todo=Todo.query.all()

    return render_template("index.html", all_todo=all_todo)



@app.route("/delete/<int:sno>")
def deleting(sno):
    deleted_todo=Todo.query.get_or_404(sno)
    db.session.delete(deleted_todo)
    db.session.commit()
    return redirect("/")


if __name__== "__main__":
    app.run(debug=True, port = 5000)