from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from stories import stories

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Show list-of-stories form."""
    return render_template("select-story.html", stories=stories.values())


@app.route("/questions", methods=["GET", "POST"])
def ask_questions():
    """Generate and show form to ask words for the selected story."""
    if request.method == "POST":
        story_id = request.form["story_id"]
        return redirect(url_for("show_story", story_id=story_id))
    else:
        story_id = request.args.get("story_id")
        story = stories.get(story_id)
        if story:
            return render_template("questions.html", story=story)
        else:
            return "Story not found", 404


@app.route("/story/<story_id>", methods=["POST"])
def show_story(story_id):
    """Show resulting story for the provided answers."""
    story = stories.get(story_id)
    if not story:
        return "Story not found", 404

    answers = {prompt: request.form[prompt] for prompt in story.prompts}
    text = story.generate(answers)

    return render_template("story.html", title=story.title, text=text)


if __name__ == "__main__":
    app.run(debug=True)
