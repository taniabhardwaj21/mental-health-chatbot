import os
import csv
from datetime import datetime

def log_chat(session_id: str, query: str, response: str, is_crisis: bool):
    """
    Logs a chat interaction to a CSV file with timestamp, session ID, query, response, and crisis flag.

    Args:
        session_id (str): Unique session identifier for the chat.
        query (str): User message.
        response (str): Chatbot's response.
        is_crisis (bool): Whether the message contained crisis-related keywords.
    """
    
    log_file = "chat_log.csv"
    file_exists = os.path.isfile(log_file)

    # Open file in append mode; create if not exists
    with open(log_file, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write header if this is a new file writes column names for the first iteration
        if not file_exists:
            writer.writerow(["timestamp", "session_id", "query", "response", "crisis_flag"])

        # Write chat data row
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            session_id,
            query,
            response,
            str(is_crisis)  
        ])
