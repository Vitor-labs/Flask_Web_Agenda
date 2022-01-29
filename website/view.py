from flask import Blueprint as bp, flash, jsonify, render_template, request
from flask_login import login_required, current_user
from website.models import Note
from . import db
import json

views = bp('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('notes')

        if len(note) == 0:
            flash('Note cannot be empty', category='error')
        if len(title) == 0:
            flash('Title cannot be empty', category='error')
        else:
            new_note = Note(title=title, content=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully', category='success')

    return render_template('home.html', user=current_user)


@views.route('/about')
def about():
    return render_template('about.html')


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['note_id']
    note = Note.query.get(note_id)

    if not note:
        return json.dumps({'status': 'error', 'message': 'Note not found'})
    else:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
