<!--
  OfbDiagram.vue — Output Feedback (OFB) diagram, pure HTML/CSS.

  Usage in slides:  <OfbDiagram />  or  <OfbDiagram width="660px" height="159px" />

  OFB per stage (matches the reference layout):
      [IV|keystream]          (top label, arrow down into the box)
      key -> [block cipher]
             ↓  keystream
      plaintext -> ⊕
             ↓
        ciphertext
  Difference from CFB: the feedback wire taps the KEYSTREAM line
  (between box and XOR), so the keystream — not the ciphertext —
  feeds back into the top of the next block cipher. Wire .fb
  .w{1,2}-* lives in the NEXT stage's <v-click>.

  Sizing: width/height props (default 780x188px = this mode's native
  design space). Shared style vocabulary from mode-base.css; the cq*
  geometry below is OFB-specific:

      y=0   .top-in    (44)   y=112 .xor-row   (32)
      y=44  .box-row   (48)   y=144 .arrow-d   (20)
      y=92  .arrow-d   (20)   y=164 .out       (24)
      wire: right from the keystream line (y=108) to the boundary
            (x=260), up to y=12 (clearly above the boxes), right along
            the top to the target center, drop to y=44, down-head into
            the box top.
-->
<script setup>
defineProps({
  width:  { type: String, default: '780px' },
  height: { type: String, default: '188px' },
})
</script>

<template>
  <div
    class="mode-root ofb"
    role="img"
    aria-label="OFB: three chained stages, keystream feeds back into the top of the next block cipher"
    :style="{ width, height }"
  >

    <!-- STAGE 1 (first block: uses IV) -->
    <v-click>
      <div class="stage">
        <div class="top-in"><span class="iv">IV</span><span class="arrow-d"></span></div>
        <div class="box-row">
          <span class="key-in"><span class="key">key</span><span class="arrow-r"></span></span>
          <div class="box">block cipher</div>
        </div>
        <div class="arrow-d"></div>
        <div class="xor-row">
          <span class="plain-in"><span class="plain">plaintext</span><span class="arrow-r"></span></span>
          <span class="xor">&#8853;</span>
        </div>
        <div class="arrow-d"></div>
        <div class="out">ciphertext</div>
      </div>
    </v-click>

    <!-- STAGE 2 (chains off stage 1 keystream) -->
    <v-click>
      <!-- feedback wire: STAGE 1 keystream -> top of STAGE 2 box -->
      <div class="fb w1-right"></div>
      <div class="fb w1-up"></div>
      <div class="fb w1-top"></div>
      <div class="fb w1-drop"></div>
      <div class="fb-head-d w1-head"></div>
      <div class="stage">
        <div class="top-in"></div>
        <div class="box-row">
          <span class="key-in"><span class="key">key</span><span class="arrow-r"></span></span>
          <div class="box">block cipher</div>
        </div>
        <div class="arrow-d"></div>
        <div class="xor-row">
          <span class="plain-in"><span class="plain">plaintext</span><span class="arrow-r"></span></span>
          <span class="xor">&#8853;</span>
        </div>
        <div class="arrow-d"></div>
        <div class="out">ciphertext</div>
      </div>
    </v-click>

    <!-- STAGE 3 (last block: no outgoing wire) -->
    <v-click>
      <!-- feedback wire: STAGE 2 keystream -> top of STAGE 3 box -->
      <div class="fb w2-right"></div>
      <div class="fb w2-up"></div>
      <div class="fb w2-top"></div>
      <div class="fb w2-drop"></div>
      <div class="fb-head-d w2-head"></div>
      <div class="stage">
        <div class="top-in"></div>
        <div class="box-row">
          <span class="key-in"><span class="key">key</span><span class="arrow-r"></span></span>
          <div class="box">block cipher</div>
        </div>
        <div class="arrow-d"></div>
        <div class="xor-row">
          <span class="plain-in"><span class="plain">plaintext</span><span class="arrow-r"></span></span>
          <span class="xor">&#8853;</span>
        </div>
        <div class="arrow-d"></div>
        <div class="out">ciphertext</div>
      </div>
    </v-click>

  </div>
</template>

<style scoped src="./mode-base.css"></style>

<style scoped>
/* OFB geometry: native design space 780px wide x 188px tall
   (N native px = N/7.8 cqw horizontal, N/1.88 cqh vertical) */
.ofb .stage { height: 100cqh; }
.ofb .top-in { height: 23.4cqh; }
.ofb .box-row { height: 25.53cqh; }
.ofb .arrow-d { height: 10.64cqh; }
.ofb .xor-row { height: 17.02cqh; }
.ofb .out { height: 12.77cqh; line-height: 12.77cqh; }
.ofb .iv, .ofb .key, .ofb .plain, .ofb .out { font-size: 10.64cqh; }
.ofb .arrow-r { width: 3cqw; }
.ofb .xor { font-size: 11.7cqh; }
.ofb .box { width: 19cqw; height: 25.53cqh; font-size: 10.64cqh; }

/* feedback wire: right from the keystream line (y=108, tapping the
   2px .arrow-d line at the source stage center) to the boundary
   (x=260), up to the box-top level (y=44), right along the top to the
   target stage center, downward arrowhead. (wire k: +33.33cqw) */
.ofb .w1-right { left: 16.67cqw; top: 57.45cqh; width: 16.67cqw; height: 2px; }
.ofb .w1-up    { left: 33.33cqw; top: 6.38cqh;  width: 2px; height: 51.06cqh; }
.ofb .w1-top   { left: 33.33cqw; top: 6.38cqh;  width: 16.67cqw; height: 2px; }
.ofb .w1-drop  { left: 50cqw;    top: 6.38cqh;  width: 2px; height: 12.23cqh; }
.ofb .w1-head  { left: 50cqw;    top: 18.62cqh; }   /* point lands on the box border (y=44) */
.ofb .w2-right { left: 50cqw;    top: 57.45cqh; width: 16.67cqw; height: 2px; }
.ofb .w2-up    { left: 66.67cqw; top: 6.38cqh;  width: 2px; height: 51.06cqh; }
.ofb .w2-top   { left: 66.67cqw; top: 6.38cqh;  width: 16.67cqw; height: 2px; }
.ofb .w2-drop  { left: 83.33cqw; top: 6.38cqh;  width: 2px; height: 12.23cqh; }
.ofb .w2-head  { left: 83.33cqw; top: 18.62cqh; }
</style>
