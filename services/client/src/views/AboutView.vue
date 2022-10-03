<template>
  <div class="about">
    <h1>About</h1>

    <div>
      <h2>What is this?</h2>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc dapibus
        cursus porttitor. Class aptent taciti sociosqu ad litora torquent per
        conubia nostra, per inceptos himenaeos. In hendrerit at urna vitae
        aliquet. Proin luctus enim eget lectus fermentum congue. Sed enim
        ligula, ornare eu mi pharetra, fringilla pellentesque massa. Nulla
        laoreet pulvinar nulla in tincidunt.
      </p>
    </div>

    <div>
      <h2>Alternatives</h2>
      <p>
        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
        inceptos himenaeos. In hendrerit at urna vitae aliquet. Proin luctus
        enim eget lectus fermentum congue. Sed enim ligula, ornare eu mi
        pharetra, fringilla pellentesque massa. Nulla laoreet pulvinar nulla in
        tincidunt.
      </p>
    </div>

    <div>
      <h2>How can you contribute?</h2>
      <p>
        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
        inceptos himenaeos. In hendrerit at urna vitae aliquet. Proin luctus
        enim eget lectus fermentum congue. Sed enim ligula, ornare eu mi
        pharetra, fringilla pellentesque massa. Nulla laoreet pulvinar nulla in
        tincidunt.
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

@media (min-width: 768px) {
  div.about {
    width: 700px;
    margin: 0 auto auto auto;
    text-align: justify;
  }

  h2 {
    padding-top: 2rem;
    padding-bottom: 1rem;
  }
}
</style>
