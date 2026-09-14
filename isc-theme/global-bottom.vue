<script setup>
import logoSrc from './public/isc-logo.png'
import ccSrc from './public/CC-isc.png'
</script>

<template>
  <footer class="absolute bottom-4 w-full flex justify-center items-center gap-8 z-50 pointer-events-none">
    <img :src="logoSrc" alt="ISC Logo" class="h-10 opacity-90" />
    <img :src="ccSrc" alt="CC License" class="h-10 opacity-90" />
  </footer>
</template>
