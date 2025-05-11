from flask import Flask, render_template, request, redirect, url_for, session
import random
import datetime

app = Flask(__name__)
app.secret_key = 'une_cle_secrete_tres_difficile_a_deviner'  # Nécessaire pour les sessions

# Réponses prédéfinies pour le chatbot
responses = [
    "Bonjour! Comment puis-je vous aider aujourd'hui?",
    "C'est une question intéressante. Laissez-moi y réfléchir.",
    "Je comprends votre demande. Pouvez-vous me donner plus de détails?",
    "Merci pour votre message! Je suis là pour vous aider.",
    "Je suis désolé, je n'ai pas compris. Pourriez-vous reformuler?",
    "Bien sûr, je peux vous aider avec ça!",
    "Je traite votre demande, un instant s'il vous plaît.",
    "N'hésitez pas à me poser d'autres questions!",
    "Je suis un assistant virtuel, je ferai de mon mieux pour vous aider.",
    "C'est noté! Y a-t-il autre chose que je puisse faire pour vous?"
]

# Initialiser la session avec un message de bienvenue
@app.before_request
def before_request():
    if 'messages' not in session:
        session['messages'] = [
            {
                'text': "Bonjour! Je suis votre assistant virtuel. Comment puis-je vous aider aujourd'hui?",
                'sender': 'bot',
                'time': datetime.datetime.now().strftime('%H:%M')
            }
        ]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_message = request.form.get('user_message', '').strip()
        
        if user_message:
            # Ajouter le message de l'utilisateur à la session
            session['messages'].append({
                'text': user_message,
                'sender': 'user',
                'time': datetime.datetime.now().strftime('%H:%M')
            })
            
            # Générer une réponse du bot
            bot_response = generate_response(user_message)
            
            # Ajouter la réponse du bot à la session
            session['messages'].append({
                'text': bot_response,
                'sender': 'bot',
                'time': datetime.datetime.now().strftime('%H:%M')
            })
            
            # Sauvegarder les changements dans la session
            session.modified = True
            
        # Redirection pour éviter les problèmes de rechargement de page
        return redirect(url_for('home'))
    
    # Récupérer les messages de la session
    messages = session.get('messages', [])
    
    return render_template('index.html', messages=messages)

def generate_response(user_message):
    """Générer une réponse en fonction du message de l'utilisateur"""
    user_message = user_message.lower()
    
    if "bonjour" in user_message or "salut" in user_message:
        return "Bonjour! Comment puis-je vous aider aujourd'hui?"
    elif "merci" in user_message:
        return "De rien! C'est un plaisir de vous aider."
    elif "au revoir" in user_message or "bye" in user_message:
        return "Au revoir! À bientôt!"
    elif "?" in user_message:
        return "C'est une bonne question. Je vais essayer d'y répondre au mieux."
    else:
        # Réponse aléatoire parmi les prédéfinies
        return random.choice(responses)

@app.route('/reset')
def reset():
    """Réinitialiser la conversation"""
    if 'messages' in session:
        session.pop('messages')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)