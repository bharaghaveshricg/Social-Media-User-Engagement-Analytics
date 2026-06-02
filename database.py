"""
Social Media User Engagement Analytics
Database Initialization Module
Creates and seeds the SQLite database
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "social_media.db")


def get_connection():
    """Return a connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create schema, triggers, views and seed data if not already present."""
    conn = get_connection()
    cur = conn.cursor()

    # ── Users ──────────────────────────────────────────────────────────────
    cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS Users (
        user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT    NOT NULL UNIQUE,
        email       TEXT    NOT NULL UNIQUE,
        full_name   TEXT    NOT NULL,
        bio         TEXT,
        location    TEXT,
        joined_date TEXT    NOT NULL DEFAULT (DATE('now')),
        is_active   INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
        profile_pic TEXT    DEFAULT 'default.png'
    );

    CREATE TABLE IF NOT EXISTS Posts (
        post_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        content    TEXT    NOT NULL,
        media_url  TEXT,
        post_type  TEXT    NOT NULL DEFAULT 'text'
                           CHECK (post_type IN ('text','image','video','reel')),
        created_at TEXT    NOT NULL DEFAULT (DATETIME('now')),
        is_deleted INTEGER NOT NULL DEFAULT 0 CHECK (is_deleted IN (0,1)),
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Likes (
        like_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id  INTEGER NOT NULL,
        user_id  INTEGER NOT NULL,
        liked_at TEXT    NOT NULL DEFAULT (DATETIME('now')),
        UNIQUE (post_id, user_id),
        FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Comments (
        comment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id      INTEGER NOT NULL,
        user_id      INTEGER NOT NULL,
        parent_id    INTEGER DEFAULT NULL,
        content      TEXT    NOT NULL CHECK (LENGTH(content) >= 1),
        commented_at TEXT    NOT NULL DEFAULT (DATETIME('now')),
        FOREIGN KEY (post_id)   REFERENCES Posts(post_id)       ON DELETE CASCADE,
        FOREIGN KEY (user_id)   REFERENCES Users(user_id)       ON DELETE CASCADE,
        FOREIGN KEY (parent_id) REFERENCES Comments(comment_id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS Followers (
        follower_id  INTEGER NOT NULL,
        following_id INTEGER NOT NULL,
        followed_at  TEXT    NOT NULL DEFAULT (DATETIME('now')),
        PRIMARY KEY (follower_id, following_id),
        CHECK (follower_id != following_id),
        FOREIGN KEY (follower_id)  REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (following_id) REFERENCES Users(user_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Hashtags (
        hashtag_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag_name   TEXT    NOT NULL UNIQUE,
        created_at TEXT    NOT NULL DEFAULT (DATETIME('now'))
    );

    CREATE TABLE IF NOT EXISTS Post_Hashtags (
        post_id    INTEGER NOT NULL,
        hashtag_id INTEGER NOT NULL,
        PRIMARY KEY (post_id, hashtag_id),
        FOREIGN KEY (post_id)    REFERENCES Posts(post_id)       ON DELETE CASCADE,
        FOREIGN KEY (hashtag_id) REFERENCES Hashtags(hashtag_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Engagement (
        engagement_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id          INTEGER NOT NULL UNIQUE,
        total_likes      INTEGER NOT NULL DEFAULT 0 CHECK (total_likes >= 0),
        total_comments   INTEGER NOT NULL DEFAULT 0 CHECK (total_comments >= 0),
        total_shares     INTEGER NOT NULL DEFAULT 0 CHECK (total_shares >= 0),
        engagement_score REAL    NOT NULL DEFAULT 0.0,
        last_updated     TEXT    NOT NULL DEFAULT (DATETIME('now')),
        FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE
    );

    -- Indexes
    CREATE INDEX IF NOT EXISTS idx_posts_user_id    ON Posts(user_id);
    CREATE INDEX IF NOT EXISTS idx_likes_post_id    ON Likes(post_id);
    CREATE INDEX IF NOT EXISTS idx_likes_user_id    ON Likes(user_id);
    CREATE INDEX IF NOT EXISTS idx_comments_post_id ON Comments(post_id);
    CREATE INDEX IF NOT EXISTS idx_comments_user_id ON Comments(user_id);
    CREATE INDEX IF NOT EXISTS idx_followers_fid    ON Followers(follower_id);
    CREATE INDEX IF NOT EXISTS idx_followers_gid    ON Followers(following_id);
    CREATE INDEX IF NOT EXISTS idx_hashtag_tag_name ON Hashtags(tag_name);
    CREATE INDEX IF NOT EXISTS idx_eng_post_id      ON Engagement(post_id);

    -- Triggers
    CREATE TRIGGER IF NOT EXISTS trg_init_engagement
    AFTER INSERT ON Posts
    BEGIN
        INSERT OR IGNORE INTO Engagement(post_id,total_likes,total_comments,total_shares,engagement_score)
        VALUES (NEW.post_id,0,0,0,0.0);
    END;

    CREATE TRIGGER IF NOT EXISTS trg_like_added
    AFTER INSERT ON Likes
    BEGIN
        UPDATE Engagement
        SET total_likes      = total_likes + 1,
            engagement_score = (total_likes+1)*1.0 + total_comments*1.5 + total_shares*2.0,
            last_updated     = DATETIME('now')
        WHERE post_id = NEW.post_id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_like_removed
    AFTER DELETE ON Likes
    BEGIN
        UPDATE Engagement
        SET total_likes      = MAX(0, total_likes - 1),
            engagement_score = MAX(0,total_likes-1)*1.0 + total_comments*1.5 + total_shares*2.0,
            last_updated     = DATETIME('now')
        WHERE post_id = OLD.post_id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_comment_added
    AFTER INSERT ON Comments
    BEGIN
        UPDATE Engagement
        SET total_comments   = total_comments + 1,
            engagement_score = total_likes*1.0 + (total_comments+1)*1.5 + total_shares*2.0,
            last_updated     = DATETIME('now')
        WHERE post_id = NEW.post_id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_comment_removed
    AFTER DELETE ON Comments
    BEGIN
        UPDATE Engagement
        SET total_comments   = MAX(0, total_comments - 1),
            engagement_score = total_likes*1.0 + MAX(0,total_comments-1)*1.5 + total_shares*2.0,
            last_updated     = DATETIME('now')
        WHERE post_id = OLD.post_id;
    END;

    -- Views
    CREATE VIEW IF NOT EXISTS v_post_analytics AS
    SELECT p.post_id, u.username, u.full_name, p.content, p.post_type, p.created_at,
           e.total_likes, e.total_comments, e.total_shares, e.engagement_score
    FROM Posts p
    JOIN Users      u ON p.user_id = u.user_id
    JOIN Engagement e ON p.post_id = e.post_id
    WHERE p.is_deleted = 0;

    CREATE VIEW IF NOT EXISTS v_user_stats AS
    SELECT u.user_id, u.username, u.full_name,
           COUNT(DISTINCT p.post_id)          AS total_posts,
           COALESCE(SUM(e.total_likes),0)     AS total_likes_received,
           COALESCE(SUM(e.total_comments),0)  AS total_comments_received,
           COALESCE(SUM(e.engagement_score),0.0) AS total_engagement,
           (SELECT COUNT(*) FROM Followers f WHERE f.following_id = u.user_id) AS follower_count,
           (SELECT COUNT(*) FROM Followers f WHERE f.follower_id  = u.user_id) AS following_count
    FROM Users u
    LEFT JOIN Posts      p ON u.user_id = p.user_id AND p.is_deleted = 0
    LEFT JOIN Engagement e ON p.post_id = e.post_id
    GROUP BY u.user_id;
    """)
    conn.commit()

    # ── Seed only if empty ──────────────────────────────────────────────────
    count = cur.execute("SELECT COUNT(*) FROM Users").fetchone()[0]
    if count == 0:
        _seed(cur)
        conn.commit()
        print("✅ Database seeded with sample data.")
    else:
        print("ℹ️  Database already contains data — skipping seed.")

    conn.close()


def _seed(cur):
    users = [
        ('alex_creates','alex@mail.com','Alex Morgan','Digital creator & traveler','New York, USA','2022-01-15'),
        ('priya_codes','priya@mail.com','Priya Sharma','Software engineer by day','Bangalore, India','2022-02-20'),
        ('james_photo','james@mail.com','James Walker','Photography enthusiast','London, UK','2022-03-10'),
        ('sofia_art','sofia@mail.com','Sofia Rodriguez','Illustrator & coffee addict','Madrid, Spain','2022-04-05'),
        ('kai_fitness','kai@mail.com','Kai Tanaka','Personal trainer & nutritionist','Tokyo, Japan','2022-05-18'),
        ('emma_writes','emma@mail.com','Emma Chen','Freelance writer & bookworm','Toronto, Canada','2022-06-22'),
        ('raj_tech','raj@mail.com','Raj Patel','AI/ML researcher','Coimbatore, India','2022-07-14'),
        ('luna_music','luna@mail.com','Luna Park','Singer-songwriter','Seoul, South Korea','2022-08-30'),
        ('omar_chef','omar@mail.com','Omar Hassan','Food blogger & chef','Dubai, UAE','2022-09-11'),
        ('zoe_travels','zoe@mail.com','Zoe Williams','Solo travel vlogger','Sydney, Australia','2022-10-25'),
        ('mark_dev','mark@mail.com','Mark Johnson','Full-stack developer','Berlin, Germany','2022-11-08'),
        ('nadia_fashion','nadia@mail.com','Nadia Ali','Fashion blogger & stylist','Paris, France','2022-12-19'),
        ('carlos_sports','carlos@mail.com','Carlos Mendez','Sports analyst & fan','Mexico City, Mexico','2023-01-07'),
        ('yuki_design','yuki@mail.com','Yuki Sato','UX designer & minimalist','Osaka, Japan','2023-02-14'),
        ('amara_science','amara@mail.com','Amara Okafor','PhD student in astrophysics','Lagos, Nigeria','2023-03-29'),
        ('leo_games','leo@mail.com','Leo Kowalski','Gamer & streamer','Warsaw, Poland','2023-04-16'),
        ('nina_yoga','nina@mail.com','Nina Ivanova','Yoga instructor & mindfulness','Moscow, Russia','2023-05-21'),
        ('sam_finance','sam@mail.com','Sam Taylor','Personal finance coach','Chicago, USA','2023-06-03'),
        ('riya_dance','riya@mail.com','Riya Nair','Classical dancer & choreographer','Chennai, India','2023-07-12'),
        ('tom_comedy','tom@mail.com','Tom Brooks','Stand-up comedian & writer','Los Angeles, USA','2023-08-01'),
    ]
    cur.executemany(
        "INSERT INTO Users(username,email,full_name,bio,location,joined_date) VALUES(?,?,?,?,?,?)",
        users
    )

    hashtags = ['#photography','#travel','#fitness','#coding','#food',
                '#music','#art','#fashion','#science','#gaming',
                '#yoga','#finance','#dance','#comedy','#tech']
    cur.executemany("INSERT INTO Hashtags(tag_name) VALUES(?)", [(t,) for t in hashtags])

    posts = [
        (1,'Just finished my latest travel series from Patagonia. The landscapes were breathtaking!','image','2024-01-10 09:15:00'),
        (2,'Wrote a new algorithm for optimizing binary search trees. Open-sourced it on GitHub!','text','2024-01-11 10:30:00'),
        (3,'Golden hour at the Thames. Nothing beats shooting in natural light. #photography','image','2024-01-12 18:45:00'),
        (4,'New illustration series: Cityscapes at night. Which one is your favourite?','image','2024-01-13 14:00:00'),
        (5,'30-day bodyweight challenge starts today! No gym needed. Follow for daily updates.','video','2024-01-14 07:00:00'),
        (6,'Book review: The Pragmatic Programmer changed how I think about software. 10/10 recommend.','text','2024-01-15 11:20:00'),
        (7,'Deployed my first transformer model on edge devices. Latency dropped by 60%.','text','2024-01-16 16:00:00'),
        (8,'New single "Midnight Echo" is out now! Wrote every word during a train ride to Busan.','video','2024-01-17 20:00:00'),
        (9,"Tried recreating Gordon Ramsay's beef wellington. Took 4 hours but SO worth it.",'image','2024-01-18 13:30:00'),
        (10,'Solo trip through Southeast Asia: day 1 in Bangkok. Street food tour at 6 AM was epic!','image','2024-01-19 08:00:00'),
        (1,"Coimbatore to Ooty by road is one of India's most beautiful drives. 100% recommend.",'image','2024-01-20 10:00:00'),
        (11,'Built a REST API with FastAPI and deployed on Railway in under 2 hours.','text','2024-01-21 09:45:00'),
        (12,'Spring 2024 street style roundup. Quiet luxury is not going anywhere.','image','2024-01-22 12:00:00'),
        (13,'Champions League predictions thread. Five bold picks that will surprise you.','text','2024-01-23 21:00:00'),
        (14,"Redesigned our app's onboarding flow. Conversion rate went up 34%.",'image','2024-01-24 11:00:00'),
        (15,'The James Webb telescope just captured a galaxy cluster 10 billion light-years away.','image','2024-01-25 15:00:00'),
        (16,'Reached Diamond rank in Valorant after 200 hours. Tips for climbing below.','video','2024-01-26 22:00:00'),
        (17,'Morning sun salutation flow for beginners. 15 minutes every day changes everything.','video','2024-01-27 06:30:00'),
        (18,'Index funds vs active management: a simple comparison for 2024 investors.','text','2024-01-28 09:00:00'),
        (19,'Bharatanatyam performance recap from the Chennai festival. Overwhelmed by the response!','video','2024-01-29 19:00:00'),
        (20,'My new stand-up set about airport security is finally online. Link in bio.','video','2024-01-30 20:30:00'),
        (2,'Python vs Rust for systems programming: honest thoughts after 6 months of Rust.','text','2024-02-01 10:00:00'),
        (7,'Vector databases explained simply: why they matter for AI apps in 2024.','text','2024-02-02 14:00:00'),
        (5,'Week 2 of the challenge complete! Sharing progress photos and updated workout plan.','image','2024-02-03 08:00:00'),
        (9,'Mumbai street food vs Delhi street food. I tested both for a week.','image','2024-02-04 13:00:00'),
        (3,'Shot this sunrise over Santorini at 5 AM. Worth every second of lost sleep.','image','2024-02-05 07:00:00'),
        (6,'Writing tips I wish I knew at 22: a thread for aspiring authors.','text','2024-02-06 10:30:00'),
        (10,'Bali on a budget: complete 10-day itinerary under $800 including flights.','text','2024-02-07 09:00:00'),
        (4,"Finished the 100-day art challenge! Here's a timelapse of my growth.",'video','2024-02-08 16:00:00'),
        (11,'Docker in plain English: containers, images, volumes explained with real examples.','text','2024-02-09 11:00:00'),
    ]
    cur.executemany("INSERT INTO Posts(user_id,content,post_type,created_at) VALUES(?,?,?,?)", posts)

    likes = [
        (1,2,'2024-01-10 10:00:00'),(1,3,'2024-01-10 11:00:00'),(1,4,'2024-01-10 12:00:00'),
        (1,5,'2024-01-10 13:00:00'),(1,6,'2024-01-10 14:00:00'),(1,7,'2024-01-10 15:00:00'),
        (1,8,'2024-01-10 16:00:00'),(1,9,'2024-01-10 17:00:00'),
        (2,1,'2024-01-11 11:00:00'),(2,7,'2024-01-11 12:00:00'),(2,11,'2024-01-11 13:00:00'),
        (2,14,'2024-01-11 14:00:00'),(2,15,'2024-01-11 15:00:00'),
        (3,1,'2024-01-12 19:00:00'),(3,4,'2024-01-12 20:00:00'),(3,10,'2024-01-12 21:00:00'),
        (3,12,'2024-01-12 22:00:00'),(3,16,'2024-01-12 23:00:00'),
        (4,1,'2024-01-13 15:00:00'),(4,3,'2024-01-13 16:00:00'),(4,12,'2024-01-13 17:00:00'),
        (5,1,'2024-01-14 08:00:00'),(5,6,'2024-01-14 09:00:00'),(5,17,'2024-01-14 10:00:00'),
        (5,18,'2024-01-14 11:00:00'),(5,19,'2024-01-14 12:00:00'),(5,20,'2024-01-14 13:00:00'),
        (6,2,'2024-01-15 12:00:00'),(6,7,'2024-01-15 13:00:00'),(6,11,'2024-01-15 14:00:00'),
        (7,2,'2024-01-16 17:00:00'),(7,11,'2024-01-16 18:00:00'),(7,14,'2024-01-16 19:00:00'),
        (7,15,'2024-01-16 20:00:00'),
        (8,1,'2024-01-17 21:00:00'),(8,6,'2024-01-17 22:00:00'),(8,19,'2024-01-17 23:00:00'),
        (9,1,'2024-01-18 14:00:00'),(9,10,'2024-01-18 15:00:00'),(9,6,'2024-01-18 16:00:00'),
        (9,12,'2024-01-18 17:00:00'),(9,20,'2024-01-18 18:00:00'),
        (10,1,'2024-01-19 09:00:00'),(10,3,'2024-01-19 10:00:00'),(10,9,'2024-01-19 11:00:00'),
        (15,1,'2024-01-25 16:00:00'),(15,2,'2024-01-25 17:00:00'),(15,7,'2024-01-25 18:00:00'),
        (15,11,'2024-01-25 19:00:00'),(15,14,'2024-01-25 20:00:00'),
        (16,5,'2024-01-26 23:00:00'),(16,13,'2024-01-27 00:00:00'),
        (17,5,'2024-01-27 07:00:00'),(17,6,'2024-01-27 08:00:00'),(17,19,'2024-01-27 09:00:00'),
        (18,2,'2024-01-28 10:00:00'),(18,7,'2024-01-28 11:00:00'),(18,15,'2024-01-28 12:00:00'),
        (20,1,'2024-01-30 21:00:00'),(20,8,'2024-01-30 22:00:00'),(20,13,'2024-01-30 23:00:00'),
    ]
    cur.executemany("INSERT INTO Likes(post_id,user_id,liked_at) VALUES(?,?,?)", likes)

    comments = [
        (1,3,'Patagonia is on my bucket list! Which season did you visit?','2024-01-10 10:30:00'),
        (1,5,'Incredible shots! What camera are you using?','2024-01-10 11:30:00'),
        (1,9,'The colours are unreal. Did you edit these heavily?','2024-01-10 12:30:00'),
        (2,1,'This is super helpful. Starred the repo!','2024-01-11 11:30:00'),
        (2,11,'Nice work. Have you benchmarked against AVL trees?','2024-01-11 12:30:00'),
        (2,14,'Love when engineers open-source their work. Bookmarked!','2024-01-11 13:30:00'),
        (3,1,'This is stunning. The reflection on the water is perfect.','2024-01-12 19:30:00'),
        (3,4,'You captured the mood beautifully. Golden hour magic!','2024-01-12 20:30:00'),
        (4,1,'The lighting in the third one is insane. Well done Sofia!','2024-01-13 15:30:00'),
        (4,6,'This would look amazing as a print. Do you sell your work?','2024-01-13 16:30:00'),
        (5,1,"Starting today! Let's go!",'2024-01-14 07:30:00'),
        (5,6,'Day 1 done! Harder than I thought but loved it.','2024-01-14 08:30:00'),
        (5,17,'Love this! Going to pair it with my morning yoga routine.','2024-01-14 09:30:00'),
        (6,2,'That book changed my life too. Timeless advice.','2024-01-15 12:30:00'),
        (6,7,'Read it twice. The section on debugging is gold.','2024-01-15 13:30:00'),
        (7,2,'How did you handle quantisation? Any quality degradation?','2024-01-16 17:30:00'),
        (7,11,'This is exactly what we need for our IoT project. DM me!','2024-01-16 18:30:00'),
        (8,1,'Midnight Echo is beautiful. Replaying it on loop.','2024-01-17 21:30:00'),
        (8,19,"Your voice is incredible Luna! Can't wait for the album.",'2024-01-17 22:30:00'),
        (9,1,'That crust looks perfect! What temp did you bake at?','2024-01-18 14:30:00'),
        (9,10,'Wow this looks restaurant quality! Recipe post please!','2024-01-18 15:30:00'),
        (10,1,'Bangkok street food at 6 AM sounds like a dream!','2024-01-19 09:30:00'),
        (10,9,'Pro tip: try Soi 38 night market for the best pad thai.','2024-01-19 10:30:00'),
        (15,2,'JWST continues to blow my mind every single week.','2024-01-25 16:30:00'),
        (15,7,'The resolution on this is unreal. Science is incredible.','2024-01-25 17:30:00'),
        (15,14,"Can you imagine what's living in those galaxies?",'2024-01-25 18:30:00'),
        (16,13,'Diamond in Valorant is serious work. Congrats!','2024-01-26 23:30:00'),
        (17,5,'Starting this tomorrow morning. Need more flexibility.','2024-01-27 07:30:00'),
        (17,6,'Such a calming video. Followed you!','2024-01-27 08:30:00'),
        (18,2,'Great breakdown. What platform do you use for your index funds?','2024-01-28 10:30:00'),
        (18,15,'Simple and clear. Sharing this with my parents.','2024-01-28 11:30:00'),
        (20,8,'The airport security bit had me crying laughing.','2024-01-30 21:30:00'),
        (20,13,'Genuinely one of the best sets I have seen this year.','2024-01-30 22:30:00'),
        (22,1,'The Rust borrow checker still gives me nightmares but I get the appeal.','2024-02-01 11:00:00'),
        (22,11,'Rust for embedded systems is a game changer. Great post.','2024-02-01 12:00:00'),
        (23,2,'Pinecone vs Weaviate vs Qdrant - any preference?','2024-02-02 15:00:00'),
        (25,1,'This looks next level. Recipe?','2024-02-04 14:00:00'),
        (26,4,'Santorini at sunrise is on my list. Love this shot!','2024-02-05 08:00:00'),
        (28,1,'Just booked Bali using this guide. Thank you Zoe!','2024-02-07 10:00:00'),
        (29,3,'The progress in the timelapse is incredible. Inspiring!','2024-02-08 17:00:00'),
    ]
    cur.executemany(
        "INSERT INTO Comments(post_id,user_id,content,commented_at) VALUES(?,?,?,?)",
        comments
    )

    followers = [
        (2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),
        (1,2),(3,2),(7,2),(11,2),(14,2),(15,2),
        (1,3),(4,3),(10,3),(12,3),
        (1,4),(3,4),(6,4),
        (1,5),(6,5),(17,5),(19,5),
        (1,7),(2,7),(11,7),(14,7),(15,7),
        (1,9),(6,9),(10,9),
        (1,10),(3,10),(9,10),
        (1,15),(7,15),
    ]
    cur.executemany("INSERT OR IGNORE INTO Followers(follower_id,following_id) VALUES(?,?)", followers)

    ph = [
        (1,2),(1,1),(2,4),(2,15),(3,1),(3,2),(4,7),(5,3),(6,4),(7,4),(7,15),
        (8,6),(9,5),(10,2),(11,4),(11,15),(12,8),(13,10),(14,15),(15,9),
        (16,10),(17,11),(18,12),(19,13),(20,14),(22,4),(23,4),(23,15),(24,3),(25,5),
        (26,1),(27,4),(28,2),(29,7),(30,4),(30,15),
    ]
    cur.executemany("INSERT OR IGNORE INTO Post_Hashtags(post_id,hashtag_id) VALUES(?,?)", ph)


# ── Stored Procedure equivalents (Python functions) ────────────────────────

def sp_user_engagement_summary(user_id: int) -> dict:
    """
    Stored Procedure: Calculate total engagement summary for a user.
    Returns total posts, likes received, comments received, engagement score.
    """
    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute("""
        SELECT
            u.username,
            u.full_name,
            COUNT(DISTINCT p.post_id)            AS total_posts,
            COALESCE(SUM(e.total_likes),    0)   AS total_likes,
            COALESCE(SUM(e.total_comments), 0)   AS total_comments,
            COALESCE(SUM(e.engagement_score),0.0) AS engagement_score,
            (SELECT COUNT(*) FROM Followers f WHERE f.following_id = u.user_id) AS followers,
            (SELECT COUNT(*) FROM Followers f WHERE f.follower_id  = u.user_id) AS following
        FROM Users u
        LEFT JOIN Posts      p ON u.user_id = p.user_id AND p.is_deleted = 0
        LEFT JOIN Engagement e ON p.post_id  = e.post_id
        WHERE u.user_id = ?
        GROUP BY u.user_id
    """, (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def sp_top_trending_posts(limit: int = 5) -> list:
    """
    Stored Procedure: Get top N trending posts by engagement score.
    """
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT
            p.post_id,
            u.username,
            p.content,
            p.post_type,
            e.total_likes,
            e.total_comments,
            e.engagement_score,
            p.created_at
        FROM Engagement e
        JOIN Posts p ON e.post_id = p.post_id
        JOIN Users u ON p.user_id = u.user_id
        WHERE p.is_deleted = 0
        ORDER BY e.engagement_score DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def sp_user_feed(user_id: int, limit: int = 10) -> list:
    """
    Stored Procedure: Get feed for a user (posts from people they follow).
    """
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT
            p.post_id,
            u.username,
            p.content,
            p.post_type,
            p.created_at,
            e.total_likes,
            e.total_comments,
            e.engagement_score
        FROM Followers f
        JOIN Posts      p ON p.user_id  = f.following_id
        JOIN Users      u ON p.user_id  = u.user_id
        JOIN Engagement e ON p.post_id  = e.post_id
        WHERE f.follower_id = ? AND p.is_deleted = 0
        ORDER BY p.created_at DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


if __name__ == "__main__":
    init_db()
    print("Database ready at:", DB_PATH)
