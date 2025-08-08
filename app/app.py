from flask import Flask
import redis

app = Flask(__name__)
client = redis.Redis(host='redis_db', port=6379)

@app.route('/')
def home():
    count = client.incr('visits')
    return f"""
    <h1>CCS 3308 - Virtualization and Containers</h1>
    <p><b>Student ID:</b> 22ug2-0584</p>
    <p><b>Student name:</b> K S N K FERNANDO</p>
    <p><b>Assignment:</b> 1</p>
    <hr>
    <h2>Visit Count: {count}</h2>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

