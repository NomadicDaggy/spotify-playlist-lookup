<template>
  <div class="about">
    <h1>About</h1>

    <div>
      <h2>What is this?</h2>
      <p>
        A few years ago I was listening to a song on Spotify. I really enjoyed
        it and wanted to find more with a similar vibe, but it was hard to pin
        down the genre and the native Spotify reccomendations were useless. So I
        looked for a way to find other users playlists which contained this song
        and so would hopefully contain others like it.
      </p>
      <p>
        All I found was
        <a
          href="https://community.spotify.com/t5/Live-Ideas/Discover-Find-public-Playlists-that-contain-Song-Artist/idi-p/144576"
        >
          this forum thread
        </a>
        which just had a lot of people wanting the same, but no real commitment
        from the Spotify side.
      </p>
      <p>
        In the time it took me to start working on this, some similar tools have
        appeared but as far as I know, they only use an advanced Google search
        to find playlists by track, which can be imprecise and incomplete.
      </p>
      <p>
        In contrast, this tool maintains a database with exact playlist-track
        relationships, allowing for much more precision, but in-turn limiting
        the number of findable playlists to only those which have been added
        into the database.
      </p>
    </div>

    <div>
      <h2>Contribute</h2>
      <p>
        Feel free to contribute to this project by checking out an existing
        issue or filing a new one at
        <a
          href="https://github.com/NomadicDaggy/spotify-playlist-lookup/issues"
        >
          the site's code repository at Github
        </a>
      </p>
      <p>
        Alternatively you can fuel my coffee addiction
        <a href="https://www.buymeacoffee.com/nomadicdaggy"
          ><br />Buy Me a Coffee :)</a
        >
      </p>
    </div>

    <div>
      <h2>Contact</h2>
      <p>
        For any other inquiries you can reach me at:
        <a href="mailto:hi@dags.dev">hi@dags.dev</a>
      </p>
    </div>
  </div>
</template>

<style scoped>
div.about {
  display: flex;
  flex-direction: column;
  margin-bottom: auto;
  padding: 0 1rem;
}

h1 {
  text-align: center;
}

h2 {
  padding-top: 1rem;
}

p {
  padding: 0.5rem 0;
}

@media (min-width: 768px) {
  div.about {
    width: 700px;
    margin: 0 auto auto auto;
    text-align: justify;
  }

  h2 {
    padding-top: 2rem;
  }
}
</style>
