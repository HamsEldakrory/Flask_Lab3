import os
from flask import Blueprint, app, current_app, flash, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from flask_login import login_required
from app.main.forms import author_form, book_form
from app.models import Author, Book, db
main_blueprint = Blueprint('main', __name__,url_prefix='/')

@main_blueprint.route('/')
@main_blueprint.route('/books/')
@login_required
def book_list():
    books = Book.query.all()
    return render_template("pages/books.html", books=books)
@main_blueprint.route("/books/<int:book_id>")
@login_required
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("pages/book_detail.html", book=book)

@main_blueprint.route('/authors/')
@login_required
def author_list():
    authors = Author.query.all()
    return render_template("pages/authors.html", authors=authors)

@main_blueprint.route('/authors/<int:author_id>')
@login_required
def view_author(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template("pages/author_detail.html", author=author)

@main_blueprint.route("/add-book", methods=["GET", "POST"])
@login_required
def add_book():
    form = book_form()
    authors = Author.query.all()
    if not authors:
        flash("No authors found. Please add an author first.", "warning")
        return redirect(url_for("main.add_author")) 
    form.author_id.choices = [(author.id, author.name) for author in authors]

    if form.validate_on_submit():
        filename = None 
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        new_book = Book(
            name=form.name.data,
            description=form.description.data,
            publish_date=form.publish_date.data,
            price=form.price.data,
            appropriate_for=form.appropriate_for.data,
            image=filename,
            author_id=form.author_id.data
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("main.book_list"))
    
    return render_template("pages/add_book.html", form=form)

@main_blueprint.route("/add-author", methods=["GET", "POST"])
@login_required
def add_author():
    form = author_form()
    if form.validate_on_submit():
        new_author = Author(name=form.name.data)
        db.session.add(new_author)
        db.session.commit()
        return redirect(url_for("main.author_list"))
    return render_template("pages/add_author.html", form=form)

@main_blueprint.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = book_form(obj=book)
    authors = Author.query.all()
    form.author_id.choices = [(author.id, author.name) for author in authors]

    if form.validate_on_submit():
        book.name = form.name.data
        book.description = form.description.data
        book.publish_date = form.publish_date.data
        book.price = form.price.data
        book.appropriate_for = form.appropriate_for.data
        book.author_id = form.author_id.data
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('main.book_list'))

    return render_template('pages/edit_book.html', form=form, book=book)
@main_blueprint.route('/delete-book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('main.book_list'))

@main_blueprint.route('/edit-author/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    form = author_form(obj=author)

    if form.validate_on_submit():
        author.name = form.name.data
        db.session.commit()
        flash('Author updated successfully!', 'success')
        return redirect(url_for('main.author_list'))

    return render_template('pages/edit_author.html', form=form, author=author)
@main_blueprint.route('/delete-author/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    flash('Author deleted successfully!', 'success')
    return redirect(url_for('main.author_list'))
