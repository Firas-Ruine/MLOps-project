from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_input():
    youtube_url = request.form.get("youtube_url")  # Get input value
    # Add your logic here
    # For example, you could launch a script or perform some task with the input
    return f"Received Youtube URL: {youtube_url}"

if __name__ == "__main__":
    app.run(debug=True)
