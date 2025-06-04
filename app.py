from flask import Flask, request, session, redirect, url_for, render_template
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure key

# Function to save responses to JSON file
def save_to_json(response):
    try:
        with open('survey_responses.json', 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(response)
    with open('survey_responses.json', 'w') as f:
        json.dump(data, f, indent=4)

# Root route redirects to survey start
@app.route('/')
def home():
    return redirect(url_for('survey', step='0'))

# Survey route handling all steps
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    step = request.args.get('step', '0')

    # Step 0: Initial question
    if step == '0':
        if request.method == 'POST':
            session['step'] = '1'
            return redirect(url_for('survey', step='1'))
        return render_template('start.html')

    # Step 1: "Do you care about me?"
    elif step == '1':
        if request.method == 'POST':
            session['care_about_me'] = request.form['answer']
            next_step = '1a' if session['care_about_me'] == 'Yes' else '2'
            return redirect(url_for('survey', step=next_step))
        return render_template('question.html', question="Do you care about me?", 
                             options=["Yes", "No"])

    # Step 1a: "Then why you don't take care of me?"
    elif step == '1a':
        if request.method == 'POST':
            session['care_reason'] = request.form['answer']
            return redirect(url_for('survey', step='2'))
        return render_template('question.html', question="Then why you don't take care of me?", 
                             options=["i don't have time", "i just can't", "i don't care"])

    # Step 2: "Am I your best friend?"
    elif step == '2':
        if request.method == 'POST':
            session['best_friend'] = request.form['answer']
            return redirect(url_for('survey', step='3'))
        return render_template('question.html', question="Am I your best friend?", 
                             options=["Yes, you are my best and favorite", "No, you are not my best", 
                                      "No, you are just a normal friend", "i don't care about this friendship"])

    # Step 3: "I love you, do you love me too?"
    elif step == '3':
        if request.method == 'POST':
            session['love_me'] = request.form['answer']
            next_step = '3a' if session['love_me'] == 'No' else '4'
            return redirect(url_for('survey', step=next_step))
        return render_template('question.html', question="I love you, do you love me too?", 
                             options=["Yes, i love you", "Yes, but only as a friend", "No"])

    # Step 3a: "Whyy?"
    elif step == '3a':
        if request.method == 'POST':
            session['love_reason'] = request.form['answer']
            return redirect(url_for('survey', step='4'))
        return render_template('question.html', question="Whyy? 💔🥀", 
                             options=["i don't like you", "i just hate love"])

    # Step 4: "I want stay with you always, what about you?"
    elif step == '4':
        if request.method == 'POST':
            session['stay_together'] = request.form['answer']
            next_step = '4a' if session['stay_together'] == "i want to stay best friends, but i don't wanna marry you" else '5'
            return redirect(url_for('survey', step=next_step))
        return render_template('question.html', question="I want stay with you always, what about you?", 
                             options=["i want to stay together forever", "i want to stay best friends, but i don't wanna marry you", 
                                      "i don't care"])

    # Step 4a: "Why you don't wanna marry me?"
    elif step == '4a':
        if request.method == 'POST':
            session['marry_reason'] = request.form['answer']
            next_step = '4b' if session['marry_reason'] == "i don't want to marry anyone" else '5'
            return redirect(url_for('survey', step=next_step))
        return render_template('question.html', question="Why you don't wanna marry me?", 
                             options=["I want", "i don't like you", "you're not my type", "i don't want to marry anyone"])

    # Step 4b: "But if you had would you choose me?"
    elif step == '4b':
        if request.method == 'POST':
            session['choose_me'] = request.form['answer']
            return redirect(url_for('survey', step='5'))
        return render_template('question.html', question="But if you had would you choose me?", 
                             options=["Yes", "No"])

    # Step 5: "Can I improve myself to fit your type?"
    elif step == '5':
        if request.method == 'POST':
            session['improve_self'] = request.form['answer']
            next_step = '5a' if session['improve_self'] == 'No' else '6'
            return redirect(url_for('survey', step=next_step))
        return render_template('question.html', question="Can I improve myself to fit your type?", 
                             options=["Yes", "No"])

    # Step 5a: "Why?" (text input)
    elif step == '5a':
        if request.method == 'POST':
            session['improve_reason'] = request.form['answer']
            return redirect(url_for('survey', step='6'))
        return render_template('text_question.html', question="Why?")

    # Step 6: "How do you want this Friendship to continue?"
    elif step == '6':
        if request.method == 'POST':
            session['friendship_continue'] = request.form['answer']
            return redirect(url_for('survey', step='7'))
        return render_template('question.html', question="How do you want this Friendship to continue?", 
                             options=["it must end right now", "i will try to care about you more", 
                                      "i want to continue this way", "i don't wanna lose you, my cat"])

    # Step 7: "Any last words?" (Final step)
    elif step == '7':
        if request.method == 'POST':
            session['last_words'] = request.form['answer']
            # Save all responses to JSON
            response = {
                'ip_address': request.remote_addr,
                'user_agent': str(request.user_agent),
                'timestamp': datetime.now().isoformat(),
                'care_about_me': session.get('care_about_me'),
                'care_reason': session.get('care_reason'),
                'best_friend': session.get('best_friend'),
                'love_me': session.get('love_me'),
                'love_reason': session.get('love_reason'),
                'stay_together': session.get('stay_together'),
                'marry_reason': session.get('marry_reason'),
                'choose_me': session.get('choose_me'),
                'improve_self': session.get('improve_self'),
                'improve_reason': session.get('improve_reason'),
                'friendship_continue': session.get('friendship_continue'),
                'last_words': session.get('last_words')
            }
            save_to_json(response)
            # Redirect based on friendship_continue response
            if response['friendship_continue'] != "it must end right now":
                return redirect(url_for('contact'))
            else:
                return redirect(url_for('goodbye'))
            session.clear()
        return render_template('text_question.html', question="Any last words?")

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Goodbye page
@app.route('/goodbye')
def goodbye():
    return render_template('goodbye.html')

# Results page
@app.route('/thefinalresult')
def final_result():
    try:
        with open('survey_responses.json', 'r') as f:
            responses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        responses = []
    return render_template('results.html', responses=responses)

if __name__ == '__main__':
    app.run(debug=True)