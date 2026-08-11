from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Folder where uploaded images will be stored
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # Get the uploaded file
        file = request.files["image"]

        if file:

            # Create uploads folder if it doesn't exist
            os.makedirs(
                app.config["UPLOAD_FOLDER"],
                exist_ok=True
            )

            # Create the file path
            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            # Save the image
            file.save(filepath)

            # Temporary moderation result
            # Rekognition will replace this later
            status = "Approved"

            # Show result page
            return render_template(
                "result.html",
                image_name=file.filename,
                status=status
            )

    # Show upload page
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)