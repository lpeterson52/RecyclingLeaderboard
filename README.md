# RecyclingLeaderboard
Leaderboard service for the AI recycling helper.

Quick run notes

- Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

- Provide MongoDB settings via `.env` (the project reads `.env`):

```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=recycling_db
```

- Start a local MongoDB (Docker):

```bash
docker run -d --name mongo -p 27017:27017 mongo:6.0
```

- Run the FastAPI app with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints

- Health: GET /health
- Top N: GET /leaderboard/top/{n}
- Update score: POST /leaderboard/{user_id} with JSON `{"score": 123}`

Example requests

```bash
# update a user's score
curl -X POST "http://127.0.0.1:8000/leaderboard/USER123" \
	-H "Content-Type: application/json" \
	-d '{"score": 42}'

# get top 10
curl "http://127.0.0.1:8000/leaderboard/top/10"
```

Notes

- The app uses `MONGO_URI` and `MONGO_DB` from `.env` via `pydantic` settings.
- `_id` values returned in the API are converted to strings as `user_id`.
- If you plan to deploy, secure your MongoDB credentials and consider using managed MongoDB with proper auth.

