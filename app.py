from flask import Flask, render_template, request
import boto3
import os
import pyodbc
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# AWS settings
REGION = "us-east-1"
BUCKET_NAME = "image-moderation-project"

# AWS clients
s3 = boto3.client(
    "s3",
    region_name=REGION
)

rekognition = boto3.client(
    "rekognition",
    region_name=REGION
)


# -----------------------------
# RDS SQL Server connection
# -----------------------------
def get_db_connection():

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server},1433;"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # Get uploaded image
        file = request.files.get("image")

        if file and file.filename:

            # Create uploads folder
            os.makedirs(
                app.config["UPLOAD_FOLDER"],
                exist_ok=True
            )

            # Local file path
            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            # Save image temporarily
            file.save(filepath)

            # -----------------------------
            # Upload image to S3
            # -----------------------------
            s3.upload_file(
                filepath,
                BUCKET_NAME,
                file.filename
            )

            print("Image uploaded successfully to S3!")

            # -----------------------------
            # Amazon Rekognition
            # -----------------------------
            response = rekognition.detect_moderation_labels(
                Image={
                    "S3Object": {
                        "Bucket": BUCKET_NAME,
                        "Name": file.filename
                    }
                },
                MinConfidence=70
            )

            moderation_labels = response.get(
                "ModerationLabels",
                []
            )

            # -----------------------------
            # Determine moderation status
            # -----------------------------
            if moderation_labels:

                status = "Rejected"

                print("Moderation labels detected:")

                for label in moderation_labels:
                    print(
                        f"{label['Name']} - "
                        f"{label['Confidence']:.2f}%"
                    )

            else:

                status = "Approved"

                print("No moderation labels detected.")

            print(f"Final status: {status}")

            # -----------------------------
            # S3 URL
            # -----------------------------
            s3_url = (
                f"https://{BUCKET_NAME}.s3.amazonaws.com/"
                f"{file.filename}"
            )

            # -----------------------------
            # Save result to RDS
            # -----------------------------
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO UploadHistory
                (ImageName, Status, S3URL)
                VALUES (?, ?, ?)
                """,
                (
                    file.filename,
                    status,
                    s3_url
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            print("Upload history saved to RDS!")

            # -----------------------------
            # Show result page
            # -----------------------------
            return render_template(
                "result.html",
                image_name=file.filename,
                status=status,
                s3_url=s3_url
            )

    return render_template("index.html")

@app.route("/history")
def history():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ID, ImageName, Status, S3URL, UploadDate
        FROM UploadHistory
        ORDER BY UploadDate DESC
    """)

    uploads = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "history.html",
        uploads=uploads
    )

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
