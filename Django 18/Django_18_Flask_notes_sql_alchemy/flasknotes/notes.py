from flask import request,  redirect, url_for, render_template, flash, Blueprint

from flasknotes import db
from flasknotes.demo import get_demo_user
from flasknotes.models import Note
from flasknotes.forms import NoteForm


bp = Blueprint('notes', __name__)


@bp.get('/')
def home():
    return redirect(url_for("notes.get_notes"))


@bp.get("/notes")
def get_notes():
    notes = db.session.execute(db.select(Note).order_by(Note.created_at.desc())).scalars().all()
    return render_template("notes/list.html", notes=notes)

@bp.get("/notes/<int:note_id>")
def note_detail(note_id: int):
    note = db.get_or_404(Note, note_id)
    return render_template("notes/detail.html", note=note)


@bp.route("/notes/create", methods=["GET","POST"])
def create_note():
    form = NoteForm()
    if form.validate_on_submit():

        note = Note(
            title=form.title.data,
            content=form.content.data,
            author=get_demo_user(),
        )
        try:
            db.session.add(note)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        flash("Note created", "success")
        return redirect(url_for("notes.note_detail", note_id=note.id))
    return render_template("notes/form.html", form=form, mode='create')



@bp.route("/notes/<int:note_id>/edit", methods=["GET","POST"])
def edit_note(note_id: int):
    note = db.get_or_404(Note, note_id)
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data.strip()
        note.content = form.content.data.strip()
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        flash("Note updated", "success")
        return redirect(url_for("notes.note_detail", note_id=note.id))
    return render_template("notes/form.html", form=form, note=note)


@bp.route("/notes/<int:note_id>/delete", methods=["GET","POST"])
def delete_note(note_id: int):
    note = db.get_or_404(Note, note_id)
    if request.method == "POST":
        try:
            db.session.delete(note)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        flash("Note deleted", "success")
        return redirect(url_for("notes.get_notes"))
    return render_template('notes/confirm_delete.html', note=note)
