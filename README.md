# Spotify playlist lookup

Service that allows lookup of Spotify playlists by songs that they contain. 

Site available in BETA at https://playlists.dags.dev

Upstream: https://github.com/NomadicDaggy/flask-on-docker

## Rough plans (in no particular order)

### Technical

- [x] **Database Migrations** - Needed for persistent prod db to update it without a hassle or data loss
- [x] **Templates** - Together with WTForms, enables easy page creation
- [x] **App Factory** - Enables setting up a separate app for each test
- [x] **Tests** - Needs the scaffolding and refactoring for testing to work at all
- [x] **Hot Reload** - Make the dev app hot-reloadable for way easier front-end development
- [x] **Analytics** - Add something like Google Analytics, but not that
- [x] **Background Tasks** - Add Celery and RabbitMQ, get user playlists in the background
- [ ] **RESTful API** - Split out the API for playlist import/search and use it from the front-end #16
- [ ] **JSON Schema** - Add JSON Schema validation #17
- [ ] **Async** - Currently the server can serve only 1 client at a time, so a large playlist import might block other users
- [ ] **Logs** - docker-compose does logging, but the logs are not persisted anywhere
- [ ] **Proper Error Handling** - Any exception shows up to users as an *Internal Server Error*
- [ ] **Comprehensive Tests** - Tests with reasonable coverage (and testing coverage as a thing we check)
- [ ] **CI & CD** - Automatically test and deploy the main branch if tests pass

### App features

- [x] **Style** - The front-end — literally anything other than plain HTML
- [x] **Playlist Import** - Importing playlists from the client
- [x] **Track Search** - Searching playlists by tracks from the client
- [ ] **Spotify Login** - Allow login with Spotify and automatically import user playlists
- [ ] **Playlist Updates** - Periodically update oldest playlists with their new tracks (as a job of some sort)
- [ ] **Mobile Front-End** - The layout is currently not responsive

## Usage

### First setup

Requires docker and docker-compose.

Fill `.env.spotify` with your apps details.

For running tests, use `test_run.sh`.

For running the development version, see `dev_run.sh`.

For production deployment, use `prod_run.sh`, but that also requires `.env.prod` and `.env.prod.db` to be created and filled.

### Commonly needed things

The dev app is visible at `localhost:1337`

You can connect to the dev database with `docker-compose exec db psql --username=spotify_playlist_lookup --dbname=spotify_playlist_lookup_dev`

And see server logs with `docker-compose logs -f`

New migration with running dev container with `docker-compose exec web flask db migrate -m "reason for migration"`
