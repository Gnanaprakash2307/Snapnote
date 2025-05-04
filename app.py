import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import config
from utils.ocr import extract_text_from_image
from utils.pdf_genarator import generate_pdf
from utils.summarizer import summarize_text
from utils.translator import translate_text_libre

app = Flask(__name__)
app.config.from_object(config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SAVED_NOTES_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple authentication for demo purposes
        # In a real app, use proper authentication with hashed passwords
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get all saved notes
    notes = []
    notes_dir = app.config['SAVED_NOTES_FOLDER']
    if os.path.exists(notes_dir):
        for filename in os.listdir(notes_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(notes_dir, filename), 'r') as f:
                    content = f.read()
                    title = filename.replace('.txt', '')
                    notes.append({
                        'title': title,
                        'content': content[:100] + '...' if len(content) > 100 else content,
                        'filename': filename
                    })

    return render_template('dashboard.html', notes=notes)


@app.route('/note/new', methods=['GET', 'POST'])
def new_note():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Save the note
        filename = secure_filename(f"{title}.txt")
        with open(os.path.join(app.config['SAVED_NOTES_FOLDER'], filename), 'w') as f:
            f.write(content)

        flash('Note saved successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', new_note=True)


@app.route('/note/<filename>')
def view_note(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        with open(os.path.join(app.config['SAVED_NOTES_FOLDER'], filename), 'r') as f:
            content = f.read()
        title = filename.replace('.txt', '')
        return render_template('dashboard.html', view_note=True,
                               note={'title': title, 'content': content, 'filename': filename})
    except:
        flash('Note not found.', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/note/edit/<filename>', methods=['GET', 'POST'])
def edit_note(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Remove old file if title changed
        old_path = os.path.join(app.config['SAVED_NOTES_FOLDER'], filename)
        if os.path.exists(old_path):
            os.remove(old_path)

        # Save with new title
        new_filename = secure_filename(f"{title}.txt")
        with open(os.path.join(app.config['SAVED_NOTES_FOLDER'], new_filename), 'w') as f:
            f.write(content)

        flash('Note updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    # Load the note for editing
    try:
        with open(os.path.join(app.config['SAVED_NOTES_FOLDER'], filename), 'r') as f:
            content = f.read()
        title = filename.replace('.txt', '')
        return render_template('dashboard.html', edit_note=True,
                               note={'title': title, 'content': content, 'filename': filename})
    except:
        flash('Note not found.', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/note/delete/<filename>')
def delete_note(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        os.remove(os.path.join(app.config['SAVED_NOTES_FOLDER'], filename))
        flash('Note deleted successfully!', 'success')
    except:
        flash('Failed to delete note.', 'danger')

    return redirect(url_for('dashboard'))


@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract text using OCR
            try:
                extracted_text = extract_text_from_image(filepath)
                return render_template('dashboard.html', ocr=True, extracted_text=extracted_text)
            except Exception as e:
                flash(f'OCR error: {str(e)}', 'danger')
                return redirect(url_for('dashboard'))

    return render_template('dashboard.html', ocr=True)


@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        text = request.form['text']
        if text:
            try:
                summary = summarize_text(text)
                return render_template('dashboard.html', summarize=True, original_text=text, summary=summary)
            except Exception as e:
                flash(f'Summarization error: {str(e)}', 'danger')
                return redirect(url_for('dashboard'))

    return render_template('dashboard.html', summarize=True)


@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        text = request.form['text']
        target_language = request.form['language']

        if text and target_language:
            try:
                translated = translate_text_libre(text, target_language)

                return render_template('dashboard.html', translate=True, original_text=text,
                                       translated_text=translated, target_language=target_language)
            except Exception as e:
                flash(f'Translation error: {str(e)}', 'danger')
                return redirect(url_for('dashboard'))

    return render_template('dashboard.html', translate=True)


@app.route('/export-pdf', methods=['GET', 'POST'])
def export_pdf():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if title and content:
            try:
                pdf_path = generate_pdf(title, content)
                # In a real app, you would return the PDF file for download
                flash('PDF generated successfully!', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f'PDF generation error: {str(e)}', 'danger')
                return redirect(url_for('dashboard'))

    return render_template('dashboard.html', export_pdf=True)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])