from flask import Flask, session, request, redirect, render_template
import datetime
import random

app = Flask(__name__)
app.secret_key= 'imaninjaimahoodyninja'


def slots():
    win = random.randrange(0, 2)
    if win == 1:
        return True
    else:
        return False

def activity(amount, outcome, location):
    onClock = datetime.datetime.now()
    if location == 'casino':
        if outcome == 'earned':
            earned = 'Entered a casino and earned %d gold... %s' % (amount, onClock)
            session['activity'].append(['earn', earned])
        elif outcome == 'lost':
            lost = 'Entered a casino and lost %d gold... Ouch.. %s' % (amount, onClock)
            session['activity'].append(['lost', lost])
        else:
            print "error"
    elif location == 'farm':
        session['activity'].append(['earn', 'Earned %d from the %s! %s' % (amount, location, onClock)])
    elif location == 'cave':
        session['activity'].append(['earn', 'Earned %d from the %s! %s' % (amount, location, onClock)])
    elif location == 'house':
        session['activity'].append(['earn', 'Earned %d from the %s! %s' % (amount, location, onClock)])


@app.route('/')    
def start():
    if 'purse' not in session:
        session['purse'] = 0
    
    if 'activity' not in session:
        session['activity'] = []
    return render_template('index.html', purse = session['purse'], activities = session['activity'])


@app.route('/process_money', methods = ['POST'])
def get_gold():
    
    hiddenVal = request.form['hidden']
    if hiddenVal == 'farm':
        farmGold = random.randrange(10, 21)
        session['purse'] += farmGold
        activity(farmGold, 'earned', 'farm')
   
    elif hiddenVal == 'cave':
        caveGold = random.randrange(5, 10)
        session['purse'] += caveGold
        activity(caveGold, 'earned', 'cave')
    
    elif hiddenVal == 'house':
        houseGold = random.randrange(2, 5)
        session['purse'] += houseGold
        activity(houseGold, 'earned', 'house')
    
    elif hiddenVal == 'casino':
        casinoGold = random.randrange(-50, 50)
        win = slots()
        if win == True:
            session['purse'] += casinoGold
            activity(casinoGold, 'earned', 'casino')
        elif win == False:
            session['purse'] -= casinoGold
            activity(casinoGold, 'lost', 'casino')
    return redirect('/')

@app.route('/restart', methods=['POST'])
def restart():
    session['purse'] = 0
    session['activity'] = []
    return redirect('/')



app.run(debug=True)