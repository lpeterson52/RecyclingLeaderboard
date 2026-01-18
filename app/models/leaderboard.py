from datetime import datetime

def leaderboard_document(user_id: str, username: str, score: int) -> dict:
    """
    Create a leaderboard document for a user.

    Args:
        user_id (str): The unique identifier for the user.
        username (str): The username of the user.
        score (int): The score of the user.

    Returns:
        dict: A dictionary representing the leaderboard document.
    """
    return {
        "user_id": user_id,
        "username": username,
        "score": score,
        "last_updated": datetime.utcnow()
    }