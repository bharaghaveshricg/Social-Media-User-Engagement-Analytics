-- ============================================================
-- Social Media User Engagement Analytics
-- Database Schema - SQLite Compatible
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLE: Users
-- Stores platform user profiles
-- ============================================================
CREATE TABLE IF NOT EXISTS Users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE,
    email         TEXT    NOT NULL UNIQUE,
    full_name     TEXT    NOT NULL,
    bio           TEXT,
    location      TEXT,
    joined_date   TEXT    NOT NULL DEFAULT (DATE('now')),
    is_active     INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    profile_pic   TEXT    DEFAULT 'default.png'
);

-- ============================================================
-- TABLE: Posts
-- Stores user-created content
-- ============================================================
CREATE TABLE IF NOT EXISTS Posts (
    post_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL,
    content       TEXT    NOT NULL,
    media_url     TEXT,
    post_type     TEXT    NOT NULL DEFAULT 'text' CHECK (post_type IN ('text','image','video','reel')),
    created_at    TEXT    NOT NULL DEFAULT (DATETIME('now')),
    is_deleted    INTEGER NOT NULL DEFAULT 0 CHECK (is_deleted IN (0, 1)),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- TABLE: Likes
-- Tracks which user liked which post
-- ============================================================
CREATE TABLE IF NOT EXISTS Likes (
    like_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id       INTEGER NOT NULL,
    user_id       INTEGER NOT NULL,
    liked_at      TEXT    NOT NULL DEFAULT (DATETIME('now')),
    UNIQUE (post_id, user_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- TABLE: Comments
-- Stores comments made on posts
-- ============================================================
CREATE TABLE IF NOT EXISTS Comments (
    comment_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id       INTEGER NOT NULL,
    user_id       INTEGER NOT NULL,
    parent_id     INTEGER DEFAULT NULL,
    content       TEXT    NOT NULL CHECK (LENGTH(content) >= 1),
    commented_at  TEXT    NOT NULL DEFAULT (DATETIME('now')),
    FOREIGN KEY (post_id)   REFERENCES Posts(post_id)    ON DELETE CASCADE,
    FOREIGN KEY (user_id)   REFERENCES Users(user_id)    ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES Comments(comment_id) ON DELETE SET NULL
);

-- ============================================================
-- TABLE: Followers
-- M:N relationship — users following other users
-- ============================================================
CREATE TABLE IF NOT EXISTS Followers (
    follower_id   INTEGER NOT NULL,
    following_id  INTEGER NOT NULL,
    followed_at   TEXT    NOT NULL DEFAULT (DATETIME('now')),
    PRIMARY KEY (follower_id, following_id),
    CHECK (follower_id != following_id),
    FOREIGN KEY (follower_id)  REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- TABLE: Hashtags
-- Master list of hashtags
-- ============================================================
CREATE TABLE IF NOT EXISTS Hashtags (
    hashtag_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name      TEXT    NOT NULL UNIQUE,
    created_at    TEXT    NOT NULL DEFAULT (DATETIME('now'))
);

-- ============================================================
-- TABLE: Post_Hashtags
-- M:N bridge between Posts and Hashtags
-- ============================================================
CREATE TABLE IF NOT EXISTS Post_Hashtags (
    post_id       INTEGER NOT NULL,
    hashtag_id    INTEGER NOT NULL,
    PRIMARY KEY (post_id, hashtag_id),
    FOREIGN KEY (post_id)    REFERENCES Posts(post_id)    ON DELETE CASCADE,
    FOREIGN KEY (hashtag_id) REFERENCES Hashtags(hashtag_id) ON DELETE CASCADE
);

-- ============================================================
-- TABLE: Engagement
-- Aggregated engagement stats per post (maintained by triggers)
-- ============================================================
CREATE TABLE IF NOT EXISTS Engagement (
    engagement_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id         INTEGER NOT NULL UNIQUE,
    total_likes     INTEGER NOT NULL DEFAULT 0 CHECK (total_likes >= 0),
    total_comments  INTEGER NOT NULL DEFAULT 0 CHECK (total_comments >= 0),
    total_shares    INTEGER NOT NULL DEFAULT 0 CHECK (total_shares >= 0),
    engagement_score REAL   NOT NULL DEFAULT 0.0,
    last_updated    TEXT    NOT NULL DEFAULT (DATETIME('now')),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE
);

-- ============================================================
-- INDEXES — for performance on frequent lookups
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_posts_user_id    ON Posts(user_id);
CREATE INDEX IF NOT EXISTS idx_likes_post_id    ON Likes(post_id);
CREATE INDEX IF NOT EXISTS idx_likes_user_id    ON Likes(user_id);
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON Comments(post_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON Comments(user_id);
CREATE INDEX IF NOT EXISTS idx_followers_fid    ON Followers(follower_id);
CREATE INDEX IF NOT EXISTS idx_followers_gid    ON Followers(following_id);
CREATE INDEX IF NOT EXISTS idx_hashtag_tag_name ON Hashtags(tag_name);
CREATE INDEX IF NOT EXISTS idx_eng_post_id      ON Engagement(post_id);

-- ============================================================
-- TRIGGER 1: Auto-insert Engagement row when Post is created
-- ============================================================
CREATE TRIGGER IF NOT EXISTS trg_init_engagement
AFTER INSERT ON Posts
BEGIN
    INSERT OR IGNORE INTO Engagement (post_id, total_likes, total_comments, total_shares, engagement_score)
    VALUES (NEW.post_id, 0, 0, 0, 0.0);
END;

-- ============================================================
-- TRIGGER 2: Update engagement when a Like is added
-- ============================================================
CREATE TRIGGER IF NOT EXISTS trg_like_added
AFTER INSERT ON Likes
BEGIN
    UPDATE Engagement
    SET total_likes      = total_likes + 1,
        engagement_score = (total_likes + 1) * 1.0 + total_comments * 1.5 + total_shares * 2.0,
        last_updated     = DATETIME('now')
    WHERE post_id = NEW.post_id;
END;

-- ============================================================
-- TRIGGER 3: Update engagement when a Like is removed
-- ============================================================
CREATE TRIGGER IF NOT EXISTS trg_like_removed
AFTER DELETE ON Likes
BEGIN
    UPDATE Engagement
    SET total_likes      = MAX(0, total_likes - 1),
        engagement_score = MAX(0, (total_likes - 1)) * 1.0 + total_comments * 1.5 + total_shares * 2.0,
        last_updated     = DATETIME('now')
    WHERE post_id = OLD.post_id;
END;

-- ============================================================
-- TRIGGER 4: Update engagement when a Comment is added
-- ============================================================
CREATE TRIGGER IF NOT EXISTS trg_comment_added
AFTER INSERT ON Comments
BEGIN
    UPDATE Engagement
    SET total_comments   = total_comments + 1,
        engagement_score = total_likes * 1.0 + (total_comments + 1) * 1.5 + total_shares * 2.0,
        last_updated     = DATETIME('now')
    WHERE post_id = NEW.post_id;
END;

-- ============================================================
-- TRIGGER 5: Update engagement when a Comment is deleted
-- ============================================================
CREATE TRIGGER IF NOT EXISTS trg_comment_removed
AFTER DELETE ON Comments
BEGIN
    UPDATE Engagement
    SET total_comments   = MAX(0, total_comments - 1),
        engagement_score = total_likes * 1.0 + MAX(0, total_comments - 1) * 1.5 + total_shares * 2.0,
        last_updated     = DATETIME('now')
    WHERE post_id = OLD.post_id;
END;

-- ============================================================
-- VIEW: v_post_analytics — convenience view for queries
-- ============================================================
CREATE VIEW IF NOT EXISTS v_post_analytics AS
SELECT
    p.post_id,
    u.username,
    u.full_name,
    p.content,
    p.post_type,
    p.created_at,
    e.total_likes,
    e.total_comments,
    e.total_shares,
    e.engagement_score
FROM Posts p
JOIN Users      u ON p.user_id  = u.user_id
JOIN Engagement e ON p.post_id  = e.post_id
WHERE p.is_deleted = 0;

-- ============================================================
-- VIEW: v_user_stats — per-user aggregated stats
-- ============================================================
CREATE VIEW IF NOT EXISTS v_user_stats AS
SELECT
    u.user_id,
    u.username,
    u.full_name,
    COUNT(DISTINCT p.post_id)                        AS total_posts,
    COALESCE(SUM(e.total_likes),    0)               AS total_likes_received,
    COALESCE(SUM(e.total_comments), 0)               AS total_comments_received,
    COALESCE(SUM(e.engagement_score), 0.0)           AS total_engagement,
    (SELECT COUNT(*) FROM Followers f WHERE f.following_id = u.user_id) AS follower_count,
    (SELECT COUNT(*) FROM Followers f WHERE f.follower_id  = u.user_id) AS following_count
FROM Users u
LEFT JOIN Posts      p ON u.user_id  = p.user_id AND p.is_deleted = 0
LEFT JOIN Engagement e ON p.post_id  = e.post_id
GROUP BY u.user_id;
