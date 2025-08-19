from flask import Flask, jsonify, request
import os
import redis

app = Flask(__name__)

# Redis connection settings from environment (docker-compose sets these)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB   = int(os.getenv("REDIS_DB", "0"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# Keys
LIKED_SET_KEY = "liked_songs"       # a Redis set to store unique liked songs

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>My Music App</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #f6f8fa, #e0eafc); margin: 0; padding: 0; display: flex; justify-content: center; }
        .container { max-width: 800px; width: 90%; background: #ffffff; box-shadow: 0 8px 20px rgba(0,0,0,0.1); border-radius: 15px; padding: 30px; margin: 50px 0; }
        h1, h2 { text-align: center; color: #2c3e50; margin-bottom: 20px; }
        h2 { margin-top: 40px; font-weight: 600; font-size: 1.5rem; }
        ul { list-style-type: none; padding: 0; }
        li { display: flex; justify-content: space-between; align-items: center; background: #f1f5f9; padding: 10px 15px; margin-bottom: 10px; border-radius: 10px; transition: background 0.3s; }
        li:hover { background: #dbeafe; }
        button { background-color: #3b82f6; border: none; color: white; padding: 6px 12px; border-radius: 50%; font-size: 16px; cursor: pointer; transition: background 0.3s, transform 0.2s; }
        button:hover { background-color: #2563eb; transform: scale(1.1); }
        #liked-songs li { background: #fde68a; }
        #liked-songs li:hover { background: #fcd34d; }
        @media (max-width: 600px) {
            .container { padding: 20px; }
            li { flex-direction: column; align-items: flex-start; }
            button { margin-top: 5px; }
        }
        .bar { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
        .tag { font-size: 0.9rem; opacity: 0.7;}
    </style>
</head>
<body>
    <div class="container">
        <div class="bar">
          <h1>🎵 Music Hub</h1>
          <span class="tag">Backed by Redis</span>
        </div>

        <h2>All Songs</h2>
        <ul id="all-songs">
            <li><span>Your Song - Elton John</span><button>+</button></li>
            <li><span>Dancing Queen - ABBA</span><button>+</button></li>
            <li><span>Annie's Song - John Denver</span><button>+</button></li>
            <li><span>Country Road - John Denver</span><button>+</button></li>
            <li><span>Hallelujah - Jeff Buckley</span><button>+</button></li>
            <li><span>Lay Me Down - Sam Smith</span><button>+</button></li>
            <li><span>Somethin' Stupid - Carson Parks</span><button>+</button></li>
            <li><span>Yesterday - The Beatles</span><button>+</button></li>
            <li><span>Rain - BTS</span><button>+</button></li>
            <li><span>Falling - Harry Styles</span><button>+</button></li>
        </ul>

        <h2>Liked Songs (persisted)</h2>
        <ul id="liked-songs"></ul>
    </div>

    <script>
        const likedList = document.getElementById("liked-songs");
        const buttons = document.querySelectorAll("#all-songs button");

        async function refreshLiked() {
            const res = await fetch("/api/liked");
            const data = await res.json();
            likedList.innerHTML = "";
            data.liked.forEach(song => {
                const li = document.createElement("li");
                li.textContent = song;
                likedList.appendChild(li);
            });
        }

        buttons.forEach(btn => {
            btn.addEventListener("click", async function() {
                const songName = this.parentElement.querySelector("span").textContent;
                // POST to API to store in Redis
                await fetch("/api/like", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({ song: songName })
                });
                await refreshLiked();
            });
        });

        // Load existing likes on page load
        refreshLiked();
    </script>
</body>
</html>
"""

@app.route("/api/like", methods=["POST"])
def api_like():
    data = request.get_json(force=True) or {}
    song = data.get("song")
    if not song:
        return jsonify({"ok": False, "error": "song is required"}), 400
    # Add to Redis set (ensures uniqueness)
    r.sadd(LIKED_SET_KEY, song)
    return jsonify({"ok": True})

@app.route("/api/liked", methods=["GET"])
def api_liked():
    liked = sorted(list(r.smembers(LIKED_SET_KEY)))
    return jsonify({"liked": liked})

@app.route("/health")
def health():
    try:
        r.ping()
        return jsonify(status="ok", redis="up"), 200
    except Exception as e:
        return jsonify(status="degraded", redis="down", error=str(e)), 500

if __name__ == "__main__":
    # On container, bind to all interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)

