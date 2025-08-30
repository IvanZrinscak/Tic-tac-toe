from flask import Flask, render_template, request, redirect, url_for

from engine import Igra

app = Flask(__name__)

# Start a 3x3 two-dimensional game.
game = Igra(n=3, d=2)
game.dodajIgrace()


@app.route("/")
def index():
    board = game.dohvatiTablu()
    winner = game.get_winner()
    size = board.shape[0]
    return render_template("index.html", board=board, size=size, winner=winner)


@app.post("/move")
def move():
    row = int(request.form["row"])
    col = int(request.form["col"])
    try:
        game.make_move((row, col))
    except ValueError:
        pass
    return redirect(url_for("index"))


@app.post("/reset")
def reset():
    global game
    game = Igra(n=3, d=2)
    game.dodajIgrace()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
