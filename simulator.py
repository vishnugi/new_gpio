import random
import time
import logging
from logging.handlers import RotatingFileHandler
from database import get_connection

DEVICES = ["device_1", "device_2", "device_3"]

# Logging setup
handler = RotatingFileHandler(
    "sensor.log",
    maxBytes=5_000_000,
    backupCount=3
)

logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def simulate_sensor():
    # 30% failure simulation (to clearly see OFFLINE)
    if random.random() < 0.3:
        raise Exception("Sensor Not Responding")

    temperature = round(random.uniform(20, 35), 2)
    humidity = round(random.uniform(40, 80), 2)

    return temperature, humidity


def generate_data():
    db = None
    cursor = None

    try:
        db = get_connection()
        cursor = db.cursor()

        print("Simulator Started... Press CTRL+C to stop.")

        while True:
            device_id = random.choice(DEVICES)

            try:
                temperature, humidity = simulate_sensor()

                # ✅ NORMAL DATA
                cursor.execute(
                    "INSERT INTO readings (device_id, temperature, humidity) VALUES (%s, %s, %s)",
                    (device_id, temperature, humidity)
                )
                db.commit()

                logger.info(f"{device_id} - {temperature}°C - {humidity}%")
                print("ONLINE:", device_id, temperature, humidity)

            except Exception as sensor_error:
                logger.error(f"{device_id} ERROR: {sensor_error}")

                # ❗ INSERT NULL VALUES → means OFFLINE
                cursor.execute(
                    "INSERT INTO readings (device_id, temperature, humidity) VALUES (%s, %s, %s)",
                    (device_id, None, None)
                )
                db.commit()

                print("OFFLINE:", device_id)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 Simulator stopped safely.")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
        print("✅ Resources cleaned up.")


if __name__ == "__main__":
    generate_data()