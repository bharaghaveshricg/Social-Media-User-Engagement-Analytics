-- ============================================================
-- Social Media User Engagement Analytics
-- SQL Queries: Joins, Nested, Indexes, Procedures
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- SECTION 1: JOIN QUERIES
-- ============================================================

-- Q1: Users with their most liked posts (INNER JOIN + GROUP BY)
SELECT
    u.username,
    u.full_name,
    p.content                           AS post_content,
    COUNT(l.like_id)                    AS like_count
FROM Users u
JOIN Posts p  ON u.user_id = p.user_id
JOIN Likes l  ON p.post_id = l.post_id
WHERE p.is_deleted = 0
GROUP BY p.post_id, u.username, u.full_name, p.content
ORDER BY like_count DESC
LIMIT 10;

-- Q2: Comments with commenter usernames and post author (3-table JOIN)
SELECT
    c.comment_id,
    author.username                     AS post_author,
    commenter.username                  AS commenter,
    SUBSTR(p.content, 1, 60) || '...'  AS post_snippet,
    c.content                           AS comment_text,
    c.commented_at
FROM Comments c
JOIN Posts p               ON c.post_id  = p.post_id
JOIN Users  author         ON p.user_id  = author.user_id
JOIN Users  commenter      ON c.user_id  = commenter.user_id
ORDER BY c.commented_at DESC
LIMIT 20;

-- Q3: Hashtag popularity — posts and engagement per hashtag (JOIN + aggregation)
SELECT
    h.tag_name,
    COUNT(DISTINCT ph.post_id)          AS post_count,
    COALESCE(SUM(e.total_likes), 0)     AS total_likes,
    COALESCE(SUM(e.total_comments), 0)  AS total_comments,
    COALESCE(SUM(e.engagement_score), 0.0) AS total_engagement
FROM Hashtags h
JOIN Post_Hashtags ph ON h.hashtag_id = ph.hashtag_id
JOIN Posts         p  ON ph.post_id   = p.post_id
JOIN Engagement    e  ON p.post_id    = e.post_id
WHERE p.is_deleted = 0
GROUP BY h.tag_name
ORDER BY total_engagement DESC;

-- Q4: Full follower-following detail with mutual count (LEFT JOIN)
SELECT
    follower.username                   AS follower_username,
    following.username                  AS follows,
    f.followed_at
FROM Followers f
JOIN Users follower  ON f.follower_id  = follower.user_id
JOIN Users following ON f.following_id = following.user_id
ORDER BY f.followed_at DESC
LIMIT 20;

-- ============================================================
-- SECTION 2: NESTED / SUBQUERY QUERIES
-- ============================================================

-- Q5: Users with more followers than the platform average (correlated subquery)
SELECT
    u.username,
    u.full_name,
    u.location,
    (SELECT COUNT(*) FROM Followers f WHERE f.following_id = u.user_id) AS follower_count
FROM Users u
WHERE (SELECT COUNT(*) FROM Followers f WHERE f.following_id = u.user_id)
    > (SELECT AVG(fc) FROM (
           SELECT COUNT(*) AS fc FROM Followers GROUP BY following_id
       ))
ORDER BY follower_count DESC;

-- Q6: Posts that received more likes than the average likes per post (subquery in WHERE)
SELECT
    u.username,
    p.content,
    p.created_at,
    e.total_likes
FROM Posts p
JOIN Users      u ON p.user_id = u.user_id
JOIN Engagement e ON p.post_id = e.post_id
WHERE e.total_likes > (
    SELECT AVG(total_likes) FROM Engagement
)
ORDER BY e.total_likes DESC;

-- Q7: Users who have NEVER posted (NOT IN subquery)
SELECT
    u.username,
    u.full_name,
    u.joined_date
FROM Users u
WHERE u.user_id NOT IN (
    SELECT DISTINCT user_id FROM Posts WHERE is_deleted = 0
);

-- Q8: Top 5 most engaged posts using subquery ranking
SELECT *
FROM (
    SELECT
        u.username,
        SUBSTR(p.content, 1, 80)        AS post_preview,
        p.post_type,
        e.total_likes,
        e.total_comments,
        e.engagement_score
    FROM Engagement e
    JOIN Posts p ON e.post_id = p.post_id
    JOIN Users u ON p.user_id = u.user_id
    WHERE p.is_deleted = 0
    ORDER BY e.engagement_score DESC
) AS ranked
LIMIT 5;

-- ============================================================
-- SECTION 3: ANALYTICS QUERIES (using Views)
-- ============================================================

-- Q9: Full post analytics via view
SELECT * FROM v_post_analytics ORDER BY engagement_score DESC LIMIT 10;

-- Q10: User leaderboard via view
SELECT
    username,
    full_name,
    total_posts,
    total_likes_received,
    total_comments_received,
    total_engagement,
    follower_count,
    following_count
FROM v_user_stats
ORDER BY total_engagement DESC
LIMIT 10;

-- Q11: Most active commenters
SELECT
    u.username,
    u.full_name,
    COUNT(c.comment_id) AS comment_count
FROM Comments c
JOIN Users u ON c.user_id = u.user_id
GROUP BY u.user_id, u.username, u.full_name
ORDER BY comment_count DESC
LIMIT 10;

-- Q12: Engagement trend by post type
SELECT
    p.post_type,
    COUNT(p.post_id)                      AS post_count,
    ROUND(AVG(e.total_likes), 2)          AS avg_likes,
    ROUND(AVG(e.total_comments), 2)       AS avg_comments,
    ROUND(AVG(e.engagement_score), 2)     AS avg_engagement
FROM Posts p
JOIN Engagement e ON p.post_id = e.post_id
WHERE p.is_deleted = 0
GROUP BY p.post_type
ORDER BY avg_engagement DESC;

-- ============================================================
-- SECTION 4: INDEX PERFORMANCE (EXPLAIN QUERY PLAN)
-- ============================================================

-- Without index (conceptual — indexes already created in schema.sql)
-- EXPLAIN QUERY PLAN
-- SELECT * FROM Likes WHERE post_id = 1;

-- With index idx_likes_post_id — SQLite will show "USING INDEX"
EXPLAIN QUERY PLAN
SELECT * FROM Likes WHERE post_id = 1;

EXPLAIN QUERY PLAN
SELECT * FROM Comments WHERE user_id = 5;

EXPLAIN QUERY PLAN
SELECT * FROM Posts WHERE user_id = 1;
