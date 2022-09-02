# Spotify playlist lookup

Service, that allows lookup of Spotify playlists by songs that they contain. 

Site available in BETA at https://dags.dev

Upstream: https://github.com/NomadicDaggy/flask-on-docker

## Rough plans (in no particular order)

### Technical

- [x] **Database Migrations** - needed for persistant prod db to be able to update it without a hassle or data loss.
- [x] **Templates** - together with WTForms would enable easy page creation.
- [x] **App Factory** - enables setting up a separate app for each test.
- [x] **Tests** - need the scaffolding and refactoring for testing to work at all.
- [x] **Hot Reload** - make the dev app hot-reloadable for way easier front-end development.
- [ ] **Async** - currently the server can serve only 1 client at a time. So a large playlist import might block other users.
- [ ] **Logs** - docker-compose does logging, but the logs are not persisted anywhere.
- [ ] **Proper Error Handling** - any exception would show up to a user as an *Internal Server Error*.
- [ ] **Comprehensive Tests** - tests with reasonable coverage (and testing coverage as a thing we check).
- [ ] **CI & CD** - automatically test and deploy the main branch if tests pass.

### App features

- [x] **Style** - front-end literally anything else than plain HTML.
- [x] **Playlist Import** - importing playlists from the client.
- [x] **Track Search** - searching playlists by tracks from the client.
- [ ] **Spotify Login** - allow login with Spotify and automatically import user playlists.
- [ ] **Playlist Updates** - periodically update oldest playlists with their new tracks (as a job of some sort).

## Usage

### First setup

Requires docker and docker-compose.

Fill `.env.spotify` with your apps details.

For running tests, use `test_run.sh`.

For running the development version see `dev_run.sh`.

For production deployment use `prod_run.sh`, but that also requires `.env.prod` and `.env.prod.db` to be created and filled.

### Commonly needed things

The dev app is visible at `localhost:1337`

You can connect to the dev database with `docker-compose exec db psql --username=spotify_playlist_lookup --dbname=spotify_playlist_lookup_dev`

And see server logs with `docker-compose logs -f`

New migration from `services/web` folder with `flask db migrate -m "reason for migration"`
