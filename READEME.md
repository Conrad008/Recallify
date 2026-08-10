# Recalify | A Spaced Repetition Flashcard App

Recalify is a **desktop flashcard application** built with **Python and CustomTkinter** that uses the **SM-2 spaced repetition algorithm** to schedule reviews based on how well you actually remember each card.

## Overview
 
Most flashcard apps just show you cards in a loop. This app tracks **how well** you know each card and uses that history to calculate exactly when you should see it again — cards you know well get spaced out further, cards you struggle with come back sooner. That scheduling logic (SM-2) is implemented from scratch, not just simulated.
 
The app supports multiple user accounts on the same machine, so each person has their own private decks and review history.

## Core Features
 
### 1. User Accounts
- Create an account and log in with a username/password
- Passwords are hashed before being stored (never saved as plain text)
- Each user only sees their own decks — data is fully separated per account
### 2. Deck & Card Management
- Create, rename, and delete decks
- Add cards manually (front/back text)
- View all cards in a deck along with their current review status
### 3. CSV Import
- Bulk-import cards into a deck from a simple two-column CSV file (`front,back`)
- Malformed or empty rows are skipped automatically
- Newly imported cards enter the review cycle immediately
### 4. Spaced Repetition Reviews (SM-2 Algorithm)
- Start a review session to go through all cards currently due
- Each card: see the front → reveal the back → rate your recall from 0–5
- Based on that rating, the app recalculates:
  - **Easiness Factor** — how "easy" the card is for you
  - **Repetitions** — consecutive successful recalls
  - **Interval** — days until the card is due again
- Every review is logged with a timestamp and rating, building a full review history per card
### 5. Stats Dashboard
- Reviews over time (bar chart)
- Distribution of quality ratings (how often you recall cards well vs. poorly)
- Breakdown of cards by status: new / learning / mastered
- Charts are scoped to the logged-in user's own data

## Tech Stack
 
| Layer | Technology |
|---|---|
| UI | CustomTkinter |
| Database | SQLite |
| ORM | SQLAlchemy |
| Charts | Matplotlib (embedded in CTk) |
| Auth | Password hashing via `hashlib`/`bcrypt` |

## Project structure

```

flashcard_app/
├── main.py                # Entry point
├── database.py            # SQLite setup + queries
├── models.py               # User, Deck, Card, ReviewLog classes
├── scheduler.py             # SM-2 spaced repetition logic
├── csv_importer.py          # CSV bulk import logic
├── auth.py                   # Password hashing/verification
├── requirements.txt
└── ui/
    ├── app.py               # Main window, screen switching
    ├── login_view.py         # Login / create account screen
    ├── deck_list_view.py     # List of user's decks
    ├── deck_detail_view.py   # Cards within a deck, add/import
    ├── review_view.py        # Review session screen
    └── stats_view.py          # Charts and stats screen

```

## How the SM-2 Algorithm Works (Summary)
 
After each review, the app updates a card's scheduling data:
 
- If recall was poor (quality < 3): reset repetitions to 0, review again tomorrow
- If recall was good (quality ≥ 3): increase the interval based on repetitions and easiness factor
- Easiness factor adjusts up or down slightly depending on how easy or hard that recall felt
This means well-known cards are shown less often, and difficult cards resurface sooner — the schedule adapts to the user rather than following a fixed pattern.

## Setup & Running Locally
 
```bash
# Clone the project folder
cd flashcard_app
 
# Install dependencies
pip install -r requirements.txt
 
# Run the app
python main.py

```

## License

This project is licensed under the MIT License.

## Author
**Conrad kipngeno**