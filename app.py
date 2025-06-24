from datetime import timezone, datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pdb
import os

app=Flask(__name__, instance_relative_config=True)

# configuring DB
db_path = os.path.join("/tmp", "todoapp.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

with app.app_context():
    db.create_all()


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
    # pdb.set_trace()
    deleted_todo=Todo.query.get_or_404(sno)
    db.session.delete(deleted_todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=["POST", "GET"])
def updating(sno):
    if request.method == "POST":
        title = request.form.get("title")
        description =request.form.get("description")
        updated_todo = Todo.query.get_or_404(sno)
        updated_todo.title = title
        updated_todo.description = description
        #to add and commit the changes to db
        db.session.add(updated_todo)
        db.session.commit()
        return redirect("/")

    
    updated_todo = Todo.query.get_or_404(sno)
    return render_template("update.html", updated_todo=updated_todo)




if __name__== "__main__":
    app.run(debug=True, port = 5000)