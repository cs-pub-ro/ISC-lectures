<!--
  EcbDiagram.vue — Electronic Code Book (ECB) diagram, pure HTML/CSS.

  Usage in slides:  <EcbDiagram />  or  <EcbDiagram width="660px" height="143px" />

  ECB: three independent stages, no chaining — no IV, no XOR, no
  feedback wires. Each stage: plaintext -> block cipher (key) ->
  ciphertext.

  Sizing: width/height props (default 780x168px = this mode's native
  design space). Shared style vocabulary comes from mode-base.css
  (container, arrows, box, labels, wire primitives); the cq* geometry
  below is ECB-specific, derived from the 780x168 design space:

      y=0   .plain      (24)   y=52  .cipher-row (64)
      y=24  .arrow-d    (28)
      y=88  .arrow-d    (28)
      y=116 .out        (24)
-->
<script setup>
defineProps({
  width:  { type: String, default: '780px' },
  height: { type: String, default: '168px' },
})
</script>

<template>
  <div
    class="mode-root ecb"
    role="img"
    aria-label="ECB: three independent block-cipher stages"
    :style="{ width, height }"
  >

    <v-click>
      <div class="stage">
        <div class="plain">plaintext</div>
        <div class="arrow-d"></div>
        <div class="cipher-row">
          <span class="key-in">
            <span class="key">key</span>
            <span class="arrow-r"></span>
          </span>
          <div class="box">block cipher</div>
        </div>
        <div class="arrow-d"></div>
        <div class="out">ciphertext</div>
      </div>
    </v-click>
    <v-click>
      <div class="stage">
        <div class="plain">plaintext</div>
        <div class="arrow-d"></div>
        <div class="cipher-row">
          <span class="key-in">
            <span class="key">key</span>
            <span class="arrow-r"></span>
          </span>
          <div class="box">block cipher</div>
        </div>
        <div class="arrow-d"></div>
        <div class="out">ciphertext</div>
      </div>
    </v-click>
    <v-click>
      <div class="stage">
        <div class="plain">plaintext</div>
        <div class="arrow-d"></div>
        <div class="cipher-row">
          <span class="key-in">
            <span class="key">key</span>
            <span class="arrow-r"></span>
          </span>
          <div class="box">block cipher</div>
        </div>
        <div class="arrow-d"></div>
        <div class="out">ciphertext</div>
      </div>
    </v-click>

  </div>
</template>

<style scoped src="./mode-base.css"></style>

<style scoped>
/* ECB geometry: native design space 780px wide x 168px tall
   (N native px = N/7.8 cqw horizontal, N/1.68 cqh vertical) */
.ecb .stage { height: 100cqh; }
.ecb .plain { height: 14.29cqh; line-height: 14.29cqh; font-size: 11.9cqh; }
.ecb .out   { height: 14.29cqh; line-height: 14.29cqh; font-size: 11.9cqh; }
.ecb .key   { font-size: 11.9cqh; }
.ecb .arrow-d  { height: 16.67cqh; }
.ecb .arrow-r  { width: 3cqw; }

/* cipher row: [key ->] anchored left, [ block cipher ] centered on 50% */
.ecb .cipher-row {
  height: 38.1cqh;
  display: flex; align-items: center; justify-content: center;
  position: relative;
}
.ecb .key-in {
  position: absolute; top: 50%; transform: translateY(-50%);
  right: calc(50% + 9.5cqw);     /* 9.5cqw = half of box width */
  display: flex; align-items: center;
}
.ecb .box {
  width: 19cqw; height: 30.95cqh;
  font-size: 10.71cqh;
}
</style>
