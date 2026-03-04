from flask import Flask, render_template, jsonify
from database import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/api/data")
def get_data():
    try:
        db = get_connection()
        cursor = db.cursor()

        cursor.execute(
            "SELECT id, device_id, temperature, humidity, timestamp "
            "FROM readings ORDER BY timestamp DESC LIMIT 20"
        )

        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "device_id": row[1],
                "temperature": row[2],
                "humidity": row[3],
                "timestamp": str(row[4])
            })

        cursor.close()
        db.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)