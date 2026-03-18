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

        # ✅ Get latest record per device
        # cursor.execute("""
        #     SELECT r1.id, r1.device_id, r1.temperature, r1.humidity, r1.timestamp
        #     FROM readings r1
        #     INNER JOIN (
        #         SELECT device_id, MAX(timestamp) AS max_time
        #         FROM readings
        #         GROUP BY device_id
        #     ) r2
        #     ON r1.device_id = r2.device_id AND r1.timestamp = r2.max_time
        # """)

        cursor.execute("""
    SELECT id, device_id, temperature, humidity, timestamp
    FROM readings
    ORDER BY timestamp DESC
    LIMIT 20
""")

        rows = cursor.fetchall()

        data = []

        for row in rows:
            temperature = row[2]
            humidity = row[3]

            # ✅ STATUS LOGIC (based on NULL values)
            if temperature is None or humidity is None:
                status = "OFFLINE"
            else:
                status = "ONLINE"

            data.append({
                "id": row[0],
                "device_id": row[1],
                "temperature": temperature,
                "humidity": humidity,
                "timestamp": str(row[4]),
                "status": status
            })

        cursor.close()
        db.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8002)