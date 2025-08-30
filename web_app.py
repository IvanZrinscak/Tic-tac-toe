from flask import Flask, render_template, request, redirect, url_for

from engine import Igra

app = Flask(__name__)

game = None
dimension = None


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/start")
def start():
    global game, dimension
    dimension = int(request.form["dimension"])
    game = Igra(n=3, d=dimension)
    game.dodajIgrace()
    return redirect(url_for("play"))


@app.route("/play")
def play():
    if game is None:
        return redirect(url_for("index"))
    board = game.dohvatiTablu()
    winner = game.get_winner()
    size = board.shape[0]
    return render_template("game.html", board=board, size=size, winner=winner, dimension=dimension)


@app.post("/move")
def move():
    if game is None:
        return redirect(url_for("index"))
    row = int(request.form["row"])
    col = int(request.form["col"])
    if dimension == 3:
        layer = int(request.form["layer"])
        coords = (row, col, layer)
    else:
        coords = (row, col)
    try:
        game.make_move(coords)
    except ValueError:
        pass
    return redirect(url_for("play"))


@app.post("/reset")
def reset():
    global game
    if dimension is None:
        return redirect(url_for("index"))
    game = Igra(n=3, d=dimension)
    game.dodajIgrace()
    return redirect(url_for("play"))


if __name__ == "__main__":
    app.run(debug=True)
