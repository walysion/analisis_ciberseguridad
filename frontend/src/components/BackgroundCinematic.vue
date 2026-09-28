<template>
  <div class="video-background">
    <!-- Capa oscura para que el texto resalte -->
    <div class="overlay"></div>
    <!-- Video en loop silencioso -->
    <video autoplay loop muted playsinline class="video-element">
      <source src="https://cdn.pixabay.com/video/2020/05/25/40156-425268487_large.mp4" type="video/mp4" />
    </video>
  </div>
</template>

<style scoped>
.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1; /* Se mantiene al fondo de todo */
  overflow: hidden;
  background-color: var(--bg-black);
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--bg-overlay);
  z-index: 1;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
  opacity: 0.6; /* Un poco de transparencia extra al video */
}
</style>