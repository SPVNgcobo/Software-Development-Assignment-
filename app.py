from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            date TEXT NOT NULL,
            age INTEGER NOT NULL,
            food TEXT NOT NULL,
            eat_out INTEGER,
            watch_movies INTEGER,
            watch_tv INTEGER,
            listen_radio INTEGER
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    name = data.get("name")
    surname = data.get("surname")
    date = data.get("date")
    age = int(data.get("age"))
    foods = request.form.getlist("food")
    food_str = ", ".join(foods)
    ratings = {
        "eat_out": int(data.get("eat_out", 0)),
        "watch_movies": int(data.get("watch_movies", 0)),
        "watch_tv": int(data.get("watch_tv", 0)),
        "listen_radio": int(data.get("listen_radio", 0))
    }

    if not (name and surname and date and 5 <= age <= 120 and all(ratings.values())):
        return "Validation Failed", 400

    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO survey (name, surname, date, age, food, eat_out, watch_movies, watch_tv, listen_radio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, surname, date, age, food_str, ratings["eat_out"], ratings["watch_movies"],
          ratings["watch_tv"], ratings["listen_radio"]))
    conn.commit()
    conn.close()
    return redirect('/results')

@app.route('/results')
def results():
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    c.execute("SELECT * FROM survey")
    surveys = c.fetchall()
    conn.close()

    if not surveys:
        return render_template("results.html", message="No Surveys Available")

    total = len(surveys)
    ages = [s[4] for s in surveys]
    avg_age = round(sum(ages) / total, 1)
    oldest = max(ages)
    youngest = min(ages)

    pizza_lovers = [s for s in surveys if "Pizza" in s[5]]
    pizza_percent = round(len(pizza_lovers) / total * 100, 1)

    eat_out_avg = round(sum([s[6] for s in surveys]) / total, 1)

    return render_template("results.html", total=total, avg_age=avg_age,
                           oldest=oldest, youngest=youngest, pizza_percent=pizza_percent,
                           eat_out_avg=eat_out_avg)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
