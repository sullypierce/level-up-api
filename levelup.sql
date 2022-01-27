SELECT * FROM levelupapi_event;

SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_game;
DELETE FROM levelupapi_event;

DELETE FROM levelupapi_event;

DELETE FROM django_migrations WHERE app = levelup;
