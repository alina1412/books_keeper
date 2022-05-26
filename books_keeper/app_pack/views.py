from flask import flash, redirect, \
            render_template, request, session, url_for

from .book_manager import BookManager
from . import app
from .auth_ import login_required


@app.route("/hello", methods=["GET", "POST"])
@login_required
def hello():
    user_email = "[" + session["email"] + "]"
    bookMan = BookManager(user_email)

    if request.method == "POST":
        # TODO: Add / search entry into the database
        todo, query = get_forms()
        if todo:
            response = bookMan.process_query(todo, query)
            return switch(response)
        else:
            return redirect("/hello")
    else:
        # TODO: Display the entries in the database on index.html
        sel_all = {"author": "", "title": "", "tags": ""}
        data = bookMan.process_regexp_search(sel_all)
        # print(user_email)
        return render_template("hello.html", data=data, error="")


def get_forms():
    clear = request.form.get("show_all")
    print("clear", clear)

    if clear == "Show all table":
        query = {"author": "", "title": "", "tags": ""}
        todo = None
    else:
        author = request.form.get("p-author", type=str)
        title = request.form.get("p-title", type=str)
        tags = request.form.get("p-tags", type=str)
        todo = request.form.get("todo", type=str)
        query = {"author": author.strip(),
                 "title": title.strip(), "tags": tags.strip()}
    return (todo, query)


def switch(response):
    exceptions = ("not enough data to add",
                  "no data matches your request", "inserted")
    if response in exceptions:
        flash(response)
        return redirect("/hello")
    else:
        # todo was search, response shall be list
        return render_template("hello.html", data=response, error="")
