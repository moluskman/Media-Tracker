import sqlite3
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI()

# 2. Tell FastAPI to automatically serve your HTML/CSS/JS files
# Visiting http://127.0.0.1:8000/static/index.html will load your UI
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- YOUR DATA MODEL GOES HERE ---
# (Hint: Define a Pydantic BaseModel for your media input)


class Media(BaseModel):
    title: str
    type: str
    status: str


# --- YOUR DATABASE SETUP GOES HERE ---
with sqlite3.connect("my_database.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()


def get_db_connection():
    conn = sqlite3.connect("my_database.db")

    conn.row_factory = sqlite3.Row
    return conn


# --- YOUR ROUTE LOGIC GOES HERE (@app.get and @app.post) ---
@app.get("/api/search")
def search_database(q: str = Query(..., min_length=1)):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # prevent sql injection
        sql = "SELECT * FROM articles WHERE title LIKE ? OR content LIKE ?"
        wildcard_query = f"%{q}%"

        cursor.execute(sql, (wildcard_query, wildcard_query))
        rows = cursor.fetchall()

        # change sqlite row into python dictionary
        results = [dict(row) for row in rows]
        cursor.close()
        conn.close()

        return {"query": q, "results": results}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


@app.post("/add-media")
def add_media(media: Media):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO media (title, type, status) VALUES (?, ?, ?)",
            (media.title, media.type, media.status),
        )
        conn.commit()

        cursor.close()
        conn.close()

        return JSONResponse(content={"message": "Media added successfully"})
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
