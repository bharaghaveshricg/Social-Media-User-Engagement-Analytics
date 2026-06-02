# 📊 EngageIQ – Social Media User Engagement Analytics

## Overview

**EngageIQ** is a desktop-based Social Media User Engagement Analytics System developed using **Python**, **Tkinter**, and **SQLite**. The application simulates a social media platform where users can create posts, interact through likes and comments, track engagement metrics, and analyze user activity through a modern analytics dashboard.

The project demonstrates concepts of **Database Management Systems (DBMS)**, **SQL Queries**, **Stored Procedure Simulation**, **Data Analytics**, and **GUI Application Development**.

---

## ✨ Features

### 🏠 Dashboard

* Real-time platform statistics
* User count, post count, likes, comments, followers, and hashtags
* Trending posts leaderboard
* Live system clock

### 👤 User Management

* Add new users
* Store user profile details
* View all registered users
* Validation and duplicate prevention

### 📝 Post Management

* Create text, image, video, and reel posts
* Assign hashtags to posts
* View recently published posts
* Store post engagement metrics

### ❤️ User Interactions

* Like and unlike posts
* Add comments to posts
* Real-time engagement updates
* Activity tracking

### 📈 Analytics Dashboard

* User engagement leaderboard
* Post-type performance analysis
* Hashtag analytics
* User spotlight search
* Engagement score calculation

### 🔍 SQL Explorer

* Execute custom SQL queries
* Explore database tables
* Predefined analytical queries
* Dynamic result visualization

---

## 🛠️ Technologies Used

| Technology  | Purpose                 |
| ----------- | ----------------------- |
| Python 3.x  | Application Development |
| Tkinter     | GUI Framework           |
| SQLite      | Database Management     |
| SQL         | Data Querying           |
| ttk Widgets | Advanced UI Components  |

---

## 📂 Project Structure

```text
EngageIQ/
│
├── app.py                 # Main GUI Application
├── database.py            # Database operations and procedures
├── social_media.db        # SQLite Database
├── README.md
│
├── tables/
│   ├── Users
│   ├── Posts
│   ├── Likes
│   ├── Comments
│   ├── Followers
│   ├── Hashtags
│   └── Post_Hashtags
│
└── analytics/
    ├── User Statistics
    ├── Trending Posts
    └── Engagement Reports
```

---

## 🗄️ Database Design

### Users

Stores user profile information.

| Field       |
| ----------- |
| user_id     |
| username    |
| email       |
| full_name   |
| bio         |
| location    |
| joined_date |

### Posts

Stores user-created content.

| Field      |
| ---------- |
| post_id    |
| user_id    |
| content    |
| post_type  |
| created_at |

### Likes

Stores user likes on posts.

### Comments

Stores comments made on posts.

### Followers

Stores follower-following relationships.

### Hashtags

Stores hashtag information.

### Post_Hashtags

Many-to-many relationship between posts and hashtags.

---

## 📊 Analytics Metrics

The system calculates:

* Total Posts
* Total Likes
* Total Comments
* Follower Count
* Following Count
* Trending Score
* Engagement Score

### Engagement Formula

```text
Engagement Score =
(Total Likes × Weight) +
(Total Comments × Weight)
```

Higher scores indicate greater user engagement.

---

## 🚀 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/EngageIQ.git
cd EngageIQ
```

### Step 2: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 3: Run Application

```bash
python app.py
```

---

## 📸 Application Modules

### Dashboard

Provides platform overview and trending content.

### Add User

Create and manage social media users.

### Create Post

Publish new content with hashtags.

### Like & Comment

Simulate social media interactions.

### Analytics

View engagement insights and user statistics.

### SQL Explorer

Execute custom SQL queries for analysis.

---

## 🎯 Learning Outcomes

This project helps understand:

* Database Design
* SQL Queries
* Joins and Relationships
* Views and Stored Procedures
* CRUD Operations
* Python GUI Development
* Data Analytics
* Real-Time Dashboard Design

---

## 🔒 Error Handling

The application includes:

* Input validation
* Duplicate user detection
* SQL exception handling
* Empty field validation
* Safe database transactions

---

## 🌟 Future Enhancements

* User Authentication
* Password Encryption
* Data Visualization Charts
* Export Reports to Excel/PDF
* Dark/Light Theme Support
* REST API Integration
* Cloud Database Support
* Machine Learning Based Trend Prediction

---

## 👨‍💻 Author

Developed as a **DBMS & Python Analytics Project** to demonstrate social media engagement tracking, analytics, and database management concepts.

---

## 📄 License

This project is intended for educational and academic purposes.

Feel free to modify and extend the project for learning and research.
