# FunBookStore

**A full-stack bookstore web app built with Django.** Users can browse and search books, post their own listings with cover images, add books to a cart and check out, rate and comment on books, and manage their personal collection.

Built as a team project for a Software Engineering course at Cal State LA, Fall 2025.

<!-- Add screenshots here -->

---

## Features

- **Accounts**: registration, login/logout, and login-protected pages that redirect guests to sign in
- **Browse & search**: view all books or search by title or author
- **Post a book**: list a book with title, author, price, summary, and an uploaded cover image
- **Book details**: full summary, cover, average rating, and a comment section
     <img width="835" height="464" alt="Screenshot 2026-10-24 184120" src="https://github.com/user-attachments/assets/5729f9d0-7f91-4a06-a1c1-693d79ba8d19" />

- **Shopping cart & checkout**: session-based cart with running totals; checking out adds books to your purchases
- **My Books**: manage the books you've posted or purchased, including removing ownership
- **Ratings**: rate books from 1 to 5 stars (one rating per user, updated in place)
- **Comments**: discuss books, with the ability to delete your own comments
     <img width="924" height="447" alt="Screenshot 2026-10-24 190227" src="https://github.com/user-attachments/assets/afe7a369-ec95-42b6-90f7-58af342e1503" />

- **About Us** page introducing the team

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python, Django 5.2 |
| Frontend | Django templates, HTML, CSS, Bootstrap |
| Database | SQLite |
| Auth | Django's built-in authentication |

## Project Structure

```
bookEx_Final_Version_2025Fall/bookEx/
├── bookEx/            # Project settings, root URLs, and HTML templates
│   └── templates/
│       ├── bookMng/       # Store pages (browse, detail, cart, search, etc.)
│       └── registration/  # Login and register pages
├── bookMng/           # Main app
│   ├── models.py      # Book, Order, PurchasedBook, Comment, Rating
│   ├── views.py       # Books, search, ratings, comments
│   ├── views_cart.py  # Cart, checkout, purchases
│   ├── cart.py        # Session-based cart logic
│   └── urls.py
├── media/uploads/     # Uploaded book covers
└── manage.py
```

## Running Locally

**Requirements:** Python 3.10+

1. Clone the repo
   ```bash
   git clone https://github.com/Rabi246/FunBookStore.git
   cd FunBookStore/bookEx_Final_Version_2025Fall/bookEx
   ```
2. Create a virtual environment and install Django
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS/Linux
   ```
3. Set up the database and run the server
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
4. Open http://127.0.0.1:8000 and register an account

The repo includes a sample SQLite database with books already loaded.

## My Contributions

I'm [Samantha Vazquez](https://github.com/Rabi246). I set up and managed the repository, reviewed and merged teammates' pull requests, and built:

- **Authentication flow**: login and register page layouts, and protecting pages so guests are redirected to log in
- **Search**: the search box and title/author search results
- **My Books**: the page UI and the remove-ownership feature
- **Comment deletion**: letting users delete their own comments
- **About Us page** and site-wide layout updates
- **Book catalog**: added the starting book collection with cover images

After the class ended, I cleaned up and improved the project:

- Removed 6,000+ committed virtual environment and IDE files, and added a `.gitignore` and `requirements.txt`
- Fixed a startup crash caused by an unused dependency import
- Made the comments page reachable from the My Books panel

## Team

- [@Rabi246](https://github.com/Rabi246) (Samantha Vazquez)
- [@robert-melena](https://github.com/robert-melena)
- [@KevSheo](https://github.com/KevSheo)
- [@Eric3871](https://github.com/Eric3871)
