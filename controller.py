from flask import Flask, request, jsonify, render_template, redirect, url_for,flash,get_flashed_messages,session
import secrets
from services import UserManage,Account

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
userService = UserManage()


@app.route('/')
def index():
    message = get_flashed_messages()
    return render_template('interface_con.html', messages=message)

@app.route('/signup')
def signup():
    message = get_flashed_messages()
    return render_template('signup.html',messages=message)

@app.route('/forgot')
def forgot():
    message = get_flashed_messages()
    return render_template('mdpo.html',messages = message)

@app.route('/reset_page')
def reset_page():
    return render_template('resetpass.html')


@app.route('/home')

def home():
    email = session.get('email')
    if not email:
        flash("User not logged in.")
        return redirect(url_for('index')) 
    unread_messages_count = userService.get_unread_messages_count(email)
    return render_template('interfacebib.html', unread_messages_count=unread_messages_count)



@app.route('/auto_biog')
def auto_biog():
    return render_template('auto_biog.html')


@app.route('/auto_biog_poli')
def auto_biog_poli():
    return render_template('auto_iog_poli.html')

@app.route('/dev_pers')
def dev_pers():
    return render_template('dev_pers.html')

@app.route('/dev_pers_fin')
def dev_pers_fin():
    return render_template('dev_pers_fin.html')

@app.route('/fict_histo')
def fict_histo():
    return render_template('fict_histo.html')

@app.route('/fict_filo')
def fict_filo():
    return render_template('fict_philo.html')

@app.route('/fict_psyco')
def fict_psyco():
    return render_template('fict_psyco.html')

@app.route('/memoire')
def memoire():
    return render_template('memoire.html')

@app.route('/change_email_page')
def change_email_page():
    return render_template('change_email.html')

@app.route('/change_email', methods=['POST'])
def change_email():
    old_email = session.get('email')
    new_email = request.form.get('email1')
    if old_email and new_email:
        success = user_service.change_email(old_email, new_email)  # type: ignore
        if success:
            session.pop('email', None)
            flash("Email changed successfully. Please log in with your new email.")
            return redirect(url_for('login')) 
        else:
            flash("Failed to change email.")
    return redirect(url_for('user_info')) 


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    account = userService.auth(email, password)  # type: ignore
    if account:
        session['email'] = account.Email
        return redirect(url_for('home'))
    flash("Invalid Email or Password. Please try again.")
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    password = request.form.get('password')
    if not full_name or not email or not password:
        flash("All fields are required.")
        return redirect(url_for('signup'))
    account = userService.get_account(email)  # type: ignore
    if account is not None:
        flash("Account already exists")
        return redirect(url_for('signup'))
    new_account = Account(Email=email, Nom=full_name, password=password, id_user=0)
    userService.create_account(new_account)
    flash("Account created successfully")
    return redirect(url_for('index'))


@app.route('/reset', methods=['POST'])
def reset():
    email = request.form.get('email')
    account = userService.get_account(email)  # type: ignore
    if account is None:
        flash("Account does not exist")
        return redirect(url_for('forgot'))
    return redirect(url_for('reset_page'))

@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    password = request.form.get('password')
    account = userService.get_account(email)  # type: ignore
    if account is None:
        flash("Account does not exist")
        return redirect(url_for('forgot', error="Account does not exist"))
    userService.rest_password(email, password)  # type: ignore
    return redirect(url_for('index'))


@app.route('/change', methods=['POST'])
def change():
    email = session.get('email')
    if not email:
        flash("User not logged in")
        return redirect(url_for('home'))
    email1 = request.form.get('email1')
    if not email1:
        flash("New email is required")
        return redirect(url_for('change_email'))
    existing_account = userService.get_account(email1)  # type: ignore
    if existing_account is not None:
        flash("The new email already exists")
        return redirect(url_for('change_email'))
    account = userService.get_account(email)  # type: ignore
    if account is None:
        flash("Account does not exist")
        return redirect(url_for('index', error="Account does not exist"))
    userService.change_email(email,email1)  # type: ignore
    updated_account = userService.get_account(email1)  # type: ignore
    return render_template('user_info.html',account=updated_account)


@app.route('/read', methods=['POST'])
def read():
    book_title = request.form.get('book_title')
    book = userService.read_book(book_title)  # type: ignore
    if book is None:
        flash("Book not found")
        return redirect(url_for('home'))
    return redirect(book['book_link'])  # type: ignore

@app.route('/describe', methods=['POST'])
def describe():
    book_title = request.form.get('book_title')
    book = userService.describe_book(book_title)  # type: ignore
    if book is None:
        flash("Book not found")
        return redirect(url_for('home'))
    return render_template('book_description.html', book=book)

@app.route('/evaluer', methods=['POST'])
def evaluer():
    book_title = request.form.get('book_title')
    book = userService.describe_book(book_title)  # type: ignore
    if book is None:
        flash("Book not found")
        return redirect(url_for('home'))
    return render_template('evaluation.html', book=book)

@app.route('/rate', methods=['POST'])
def rate():
    book_id = request.form.get('book_id')
    rating = request.form.get('rating')
    if not book_id:
        flash("Book ID is missing")
        return redirect(url_for('home'))
    userService.rate(book_id,rating)  # type: ignore
    userService.update_book_ratings()
    return redirect(url_for('home'))

@app.route('/user_info', methods=['POST'])
def user_info():
    email = session.get('email')  # Retrieve email from session
    if not email:
        flash("User not logged in")
        return redirect(url_for('home'))
    account = userService.user_info(email)  # type: ignore
    if account is None:
        flash("Account not found")
        return redirect(url_for('home'))
    return render_template('user_info.html', account=account)


@app.route('/search_books', methods=['POST'])
def search_books():
    user_input = request.form.get('search_query')
    if not user_input:
        return render_template('book_description.html', book=None)
    matching_books = userService.chercher(user_input)
    if not matching_books:
        return render_template('book_description.html', book=None)
    return render_template('search_res.html', books=matching_books)


@app.route('/reception_mail', methods=['GET', 'POST'])
def reception_mail():
    email = session.get('email')
    if not email:
        flash("User not logged in.")
        return redirect(url_for('index'))
    unread_messages_count = userService.get_unread_messages_count(email)
    if request.method == 'POST':
        email_id = request.form.get('id')
        action = request.form.get('action')
        if action == 'mark_read':
            userService.mark_message_as_read(email_id)
            flash("Email marked as read.")
        elif action == 'delete':
            userService.delete_message(email_id, email)
            flash("Email deleted.")
        return redirect(url_for('reception_mail')) 
    emails = userService.get_messages(email)
    return render_template('reception_mail.html', emails=emails, unread_messages_count=unread_messages_count)







if __name__ == '__main__':
    app.run(debug=True, port=8080,host='0.0.0.0')