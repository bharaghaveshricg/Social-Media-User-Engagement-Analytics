-- ============================================================
-- Social Media User Engagement Analytics
-- Seed Data — 100+ Realistic Records
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- USERS (20 users)
-- ============================================================
INSERT INTO Users (username, email, full_name, bio, location, joined_date) VALUES
('alex_creates',   'alex@mail.com',    'Alex Morgan',     'Digital creator & traveler',   'New York, USA',      '2022-01-15'),
('priya_codes',    'priya@mail.com',   'Priya Sharma',    'Software engineer by day',      'Bangalore, India',   '2022-02-20'),
('james_photo',    'james@mail.com',   'James Walker',    'Photography enthusiast',        'London, UK',         '2022-03-10'),
('sofia_art',      'sofia@mail.com',   'Sofia Rodriguez', 'Illustrator & coffee addict',   'Madrid, Spain',      '2022-04-05'),
('kai_fitness',    'kai@mail.com',     'Kai Tanaka',      'Personal trainer & nutritionist','Tokyo, Japan',      '2022-05-18'),
('emma_writes',    'emma@mail.com',    'Emma Chen',       'Freelance writer & bookworm',   'Toronto, Canada',    '2022-06-22'),
('raj_tech',       'raj@mail.com',     'Raj Patel',       'AI/ML researcher',              'Coimbatore, India',  '2022-07-14'),
('luna_music',     'luna@mail.com',    'Luna Park',       'Singer-songwriter',             'Seoul, South Korea', '2022-08-30'),
('omar_chef',      'omar@mail.com',    'Omar Hassan',     'Food blogger & chef',           'Dubai, UAE',         '2022-09-11'),
('zoe_travels',    'zoe@mail.com',     'Zoe Williams',    'Solo travel vlogger',           'Sydney, Australia',  '2022-10-25'),
('mark_dev',       'mark@mail.com',    'Mark Johnson',    'Full-stack developer',          'Berlin, Germany',    '2022-11-08'),
('nadia_fashion',  'nadia@mail.com',   'Nadia Ali',       'Fashion blogger & stylist',     'Paris, France',      '2022-12-19'),
('carlos_sports',  'carlos@mail.com',  'Carlos Mendez',   'Sports analyst & fan',          'Mexico City, Mexico','2023-01-07'),
('yuki_design',    'yuki@mail.com',    'Yuki Sato',       'UX designer & minimalist',      'Osaka, Japan',       '2023-02-14'),
('amara_science',  'amara@mail.com',   'Amara Okafor',    'PhD student in astrophysics',   'Lagos, Nigeria',     '2023-03-29'),
('leo_games',      'leo@mail.com',     'Leo Kowalski',    'Gamer & streamer',              'Warsaw, Poland',     '2023-04-16'),
('nina_yoga',      'nina@mail.com',    'Nina Ivanova',    'Yoga instructor & mindfulness', 'Moscow, Russia',     '2023-05-21'),
('sam_finance',    'sam@mail.com',     'Sam Taylor',      'Personal finance coach',        'Chicago, USA',       '2023-06-03'),
('riya_dance',     'riya@mail.com',    'Riya Nair',       'Classical dancer & choreographer','Chennai, India',   '2023-07-12'),
('tom_comedy',     'tom@mail.com',     'Tom Brooks',      'Stand-up comedian & writer',    'Los Angeles, USA',   '2023-08-01');

-- ============================================================
-- HASHTAGS (15 hashtags)
-- ============================================================
INSERT INTO Hashtags (tag_name) VALUES
('#photography'),('#travel'),('#fitness'),('#coding'),('#food'),
('#music'),('#art'),('#fashion'),('#science'),('#gaming'),
('#yoga'),('#finance'),('#dance'),('#comedy'),('#tech');

-- ============================================================
-- POSTS (30 posts)
-- ============================================================
INSERT INTO Posts (user_id, content, post_type, created_at) VALUES
(1,  'Just finished my latest travel series from Patagonia. The landscapes were breathtaking!',            'image', '2024-01-10 09:15:00'),
(2,  'Wrote a new algorithm for optimizing binary search trees. Open-sourced it on GitHub!',              'text',  '2024-01-11 10:30:00'),
(3,  'Golden hour at the Thames. Nothing beats shooting in natural light. #photography',                   'image', '2024-01-12 18:45:00'),
(4,  'New illustration series: Cityscapes at night. Which one is your favourite?',                        'image', '2024-01-13 14:00:00'),
(5,  '30-day bodyweight challenge starts today! No gym needed. Follow for daily updates. #fitness',       'video', '2024-01-14 07:00:00'),
(6,  'Book review: The Pragmatic Programmer changed how I think about software. 10/10 recommend.',        'text',  '2024-01-15 11:20:00'),
(7,  'Deployed my first transformer model on edge devices. Latency dropped by 60%. #tech',                'text',  '2024-01-16 16:00:00'),
(8,  'New single "Midnight Echo" is out now! Wrote every word during a train ride to Busan.',             'video', '2024-01-17 20:00:00'),
(9,  'Tried recreating Gordon Ramsay''s beef wellington. Took 4 hours but SO worth it. #food',            'image', '2024-01-18 13:30:00'),
(10, 'Solo trip through Southeast Asia: day 1 in Bangkok. Street food tour at 6 AM was epic!',            'image', '2024-01-19 08:00:00'),
(1,  'Coimbatore to Ooty by road is one of India''s most beautiful drives. 100% recommend.',              'image', '2024-01-20 10:00:00'),
(11, 'Built a REST API with FastAPI and deployed on Railway in under 2 hours. Notes in thread.',          'text',  '2024-01-21 09:45:00'),
(12, 'Spring 2024 street style roundup. Quiet luxury is not going anywhere.',                             'image', '2024-01-22 12:00:00'),
(13, 'Champions League predictions thread. Five bold picks that will surprise you.',                      'text',  '2024-01-23 21:00:00'),
(14, 'Redesigned our app''s onboarding flow. Conversion rate went up 34%. Here''s what changed.',        'image', '2024-01-24 11:00:00'),
(15, 'The James Webb telescope just captured a galaxy cluster 10 billion light-years away. Insane.',      'image', '2024-01-25 15:00:00'),
(16, 'Reached Diamond rank in Valorant after 200 hours. Tips for climbing the ranked ladder below.',      'video', '2024-01-26 22:00:00'),
(17, 'Morning sun salutation flow for beginners. 15 minutes every day changes everything. #yoga',         'video', '2024-01-27 06:30:00'),
(18, 'Index funds vs active management: a simple comparison for 2024 investors.',                         'text',  '2024-01-28 09:00:00'),
(19, 'Bharatanatyam performance recap from the Chennai festival. Overwhelmed by the response!',            'video', '2024-01-29 19:00:00'),
(20, 'My new stand-up set about airport security is finally online. Link in bio.',                        'video', '2024-01-30 20:30:00'),
(2,  'Python vs Rust for systems programming: honest thoughts after 6 months of Rust.',                  'text',  '2024-02-01 10:00:00'),
(7,  'Vector databases explained simply: why they matter for AI apps in 2024.',                           'text',  '2024-02-02 14:00:00'),
(5,  'Week 2 of the challenge complete! Sharing progress photos and updated workout plan.',               'image', '2024-02-03 08:00:00'),
(9,  'Mumbai street food vs Delhi street food. I tested both for a week. Honest verdict inside.',        'image', '2024-02-04 13:00:00'),
(3,  'Shot this sunrise over Santorini at 5 AM. Worth every second of lost sleep.',                      'image', '2024-02-05 07:00:00'),
(6,  'Writing tips I wish I knew at 22: a thread for aspiring authors.',                                  'text',  '2024-02-06 10:30:00'),
(10, 'Bali on a budget: complete 10-day itinerary under $800 including flights.',                        'text',  '2024-02-07 09:00:00'),
(4,  'Finished the 100-day art challenge! Here''s a timelapse of my growth.',                             'video', '2024-02-08 16:00:00'),
(11, 'Docker in plain English: containers, images, volumes explained with real examples.',               'text',  '2024-02-09 11:00:00');

-- ============================================================
-- LIKES (60 likes spread across posts and users)
-- ============================================================
INSERT INTO Likes (post_id, user_id, liked_at) VALUES
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
(16,5,'2024-01-26 23:00:00'),(16,13,'2024-01-26 24:00:00'),
(17,5,'2024-01-27 07:00:00'),(17,6,'2024-01-27 08:00:00'),(17,19,'2024-01-27 09:00:00'),
(18,2,'2024-01-28 10:00:00'),(18,7,'2024-01-28 11:00:00'),(18,15,'2024-01-28 12:00:00'),
(20,1,'2024-01-30 21:00:00'),(20,8,'2024-01-30 22:00:00'),(20,13,'2024-01-30 23:00:00');

-- ============================================================
-- COMMENTS (40 comments)
-- ============================================================
INSERT INTO Comments (post_id, user_id, content, commented_at) VALUES
(1, 3,  'Patagonia is on my bucket list! Which season did you visit?',               '2024-01-10 10:30:00'),
(1, 5,  'Incredible shots! What camera are you using?',                               '2024-01-10 11:30:00'),
(1, 9,  'The colours are unreal. Did you edit these heavily?',                        '2024-01-10 12:30:00'),
(2, 1,  'This is super helpful. Starred the repo!',                                   '2024-01-11 11:30:00'),
(2, 11, 'Nice work. Have you benchmarked against AVL trees?',                         '2024-01-11 12:30:00'),
(2, 14, 'Love when engineers open-source their work. Bookmarked!',                    '2024-01-11 13:30:00'),
(3, 1,  'This is stunning. The reflection on the water is perfect.',                  '2024-01-12 19:30:00'),
(3, 4,  'You captured the mood beautifully. Golden hour magic!',                      '2024-01-12 20:30:00'),
(4, 1,  'The lighting in the third one is insane. Well done Sofia!',                  '2024-01-13 15:30:00'),
(4, 6,  'This would look amazing as a print. Do you sell your work?',                 '2024-01-13 16:30:00'),
(5, 1,  'Starting today! Let''s go!',                                                 '2024-01-14 07:30:00'),
(5, 6,  'Day 1 done! Harder than I thought but loved it.',                            '2024-01-14 08:30:00'),
(5, 17, 'Love this! Going to pair it with my morning yoga routine.',                  '2024-01-14 09:30:00'),
(6, 2,  'That book changed my life too. Timeless advice.',                            '2024-01-15 12:30:00'),
(6, 7,  'Read it twice. The section on debugging is gold.',                           '2024-01-15 13:30:00'),
(7, 2,  'How did you handle quantisation? Any quality degradation?',                  '2024-01-16 17:30:00'),
(7, 11, 'This is exactly what we need for our IoT project. DM me!',                   '2024-01-16 18:30:00'),
(8, 1,  'Midnight Echo is beautiful. Replaying it on loop.',                          '2024-01-17 21:30:00'),
(8, 19, 'Your voice is incredible Luna! Can''t wait for the album.',                  '2024-01-17 22:30:00'),
(9, 1,  'That crust looks perfect! What temp did you bake at?',                       '2024-01-18 14:30:00'),
(9, 10, 'Wow this looks restaurant quality! Recipe post please!',                     '2024-01-18 15:30:00'),
(10,1,  'Bangkok street food at 6 AM sounds like a dream!',                           '2024-01-19 09:30:00'),
(10,9,  'Pro tip: try Soi 38 night market for the best pad thai.',                    '2024-01-19 10:30:00'),
(15,2,  'JWST continues to blow my mind every single week.',                          '2024-01-25 16:30:00'),
(15,7,  'The resolution on this is unreal. Science is incredible.',                   '2024-01-25 17:30:00'),
(15,14, 'Can you imagine what''s living in those galaxies?',                           '2024-01-25 18:30:00'),
(16,13, 'Diamond in Valorant is serious work. Congrats!',                             '2024-01-26 23:30:00'),
(17,5,  'Starting this tomorrow morning. Need more flexibility.',                     '2024-01-27 07:30:00'),
(17,6,  'Such a calming video. Followed you!',                                        '2024-01-27 08:30:00'),
(18,2,  'Great breakdown. What platform do you use for your index funds?',            '2024-01-28 10:30:00'),
(18,15, 'Simple and clear. Sharing this with my parents.',                            '2024-01-28 11:30:00'),
(20,8,  'The airport security bit had me crying laughing.',                           '2024-01-30 21:30:00'),
(20,13, 'Genuinely one of the best sets I''ve seen this year.',                       '2024-01-30 22:30:00'),
(22,1,  'The Rust borrow checker still gives me nightmares but I get the appeal.',    '2024-02-01 11:00:00'),
(22,11, 'Rust for embedded systems is a game changer. Great post.',                   '2024-02-01 12:00:00'),
(23,2,  'Pinecone vs Weaviate vs Qdrant - any preference?',                           '2024-02-02 15:00:00'),
(25,1,  'This looks next level. Recipe?',                                             '2024-02-04 14:00:00'),
(26,4,  'Santorini at sunrise is on my list. Love this shot!',                        '2024-02-05 08:00:00'),
(28,1,  'Just booked Bali using this guide. Thank you Zoe!',                          '2024-02-07 10:00:00'),
(29,3,  'The progress in the timelapse is incredible. Inspiring!',                    '2024-02-08 17:00:00');

-- ============================================================
-- FOLLOWERS (40 follow relationships)
-- ============================================================
INSERT INTO Followers (follower_id, following_id, followed_at) VALUES
(2,1,'2024-01-16 10:00:00'),(3,1,'2024-01-17 10:00:00'),(4,1,'2024-01-18 10:00:00'),
(5,1,'2024-01-19 10:00:00'),(6,1,'2024-01-20 10:00:00'),(7,1,'2024-01-21 10:00:00'),
(8,1,'2024-01-22 10:00:00'),(9,1,'2024-01-23 10:00:00'),(10,1,'2024-01-24 10:00:00'),
(11,1,'2024-01-25 10:00:00'),
(1,2,'2024-01-16 11:00:00'),(3,2,'2024-01-17 11:00:00'),(7,2,'2024-01-18 11:00:00'),
(11,2,'2024-01-19 11:00:00'),(14,2,'2024-01-20 11:00:00'),(15,2,'2024-01-21 11:00:00'),
(1,3,'2024-01-16 12:00:00'),(4,3,'2024-01-17 12:00:00'),(10,3,'2024-01-18 12:00:00'),
(12,3,'2024-01-19 12:00:00'),
(1,4,'2024-01-16 13:00:00'),(3,4,'2024-01-17 13:00:00'),(6,4,'2024-01-18 13:00:00'),
(1,5,'2024-01-16 14:00:00'),(6,5,'2024-01-17 14:00:00'),(17,5,'2024-01-18 14:00:00'),
(19,5,'2024-01-19 14:00:00'),
(1,7,'2024-01-16 15:00:00'),(2,7,'2024-01-17 15:00:00'),(11,7,'2024-01-18 15:00:00'),
(14,7,'2024-01-19 15:00:00'),(15,7,'2024-01-20 15:00:00'),
(1,9,'2024-01-16 16:00:00'),(6,9,'2024-01-17 16:00:00'),(10,9,'2024-01-18 16:00:00'),
(1,10,'2024-01-16 17:00:00'),(3,10,'2024-01-17 17:00:00'),(9,10,'2024-01-18 17:00:00'),
(1,15,'2024-01-16 18:00:00'),(7,15,'2024-01-17 18:00:00');

-- ============================================================
-- POST_HASHTAGS (associating posts with hashtags)
-- ============================================================
INSERT INTO Post_Hashtags (post_id, hashtag_id) VALUES
(1,2),(1,1),(2,4),(2,15),(3,1),(3,2),(4,7),(5,3),(6,4),(7,4),(7,15),
(8,6),(9,5),(10,2),(11,4),(11,15),(12,8),(13,10),(14,15),(15,9),
(16,10),(17,11),(18,12),(19,13),(20,14),(22,4),(23,4),(23,15),(24,3),(25,5),
(26,1),(27,4),(28,2),(29,7),(30,4),(30,15);
