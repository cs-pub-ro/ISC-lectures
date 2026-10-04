<!--
  CfbDiagram.vue — Cipher Feedback (CFB) diagram, pure HTML/CSS.

  Usage in slides:  <CfbDiagram />  or  <CfbDiagram width="660px" height="179px" />

  CFB per stage (matches the reference layout):
      [IV|c_{i-1}]          (top label, arrow down into the box)
      key -> [block cipher] (key enters at the left-center edge)
             ↓
      plaintext -> ⊕         (plaintext feeds the XOR from the left)
             ↓
        ciphertext
  The ciphertext feeds back over the top into the TOP of the next
  block cipher (wire .fb .w{1,2}-*, lives in the NEXT stage's
  <v-click> so it only appears once its target box is visible).

  Sizing: width/height props (default 780x210px = this mode's native
  design space). Shared style vocabulary from mode-base.css; the cq*
  geometry below is CFB-specific:

      y=0   .top-in    (44)   y=112 .xor-row   (32)
      y=44  .box-row   (48)   y=144 .arrow-d   (20)
      y=92  .arrow-d   (20)   y=164 .out       (24)
      wire: down y=188..208 at source center, right to the boundary
            (x=260), up to y=12 (clearly above the boxes), right along
            the top to the target center, drop to y=44, down-head into
            the box top.
-->
<script setup>
defineProps({
  width:  { type: String, default: '780px' },
  height: { type: String, default: '210px' },
})
</script>

<template>
  <div
    class="mode-root cfb"
    role="img"
    aria-label="CFB: three chained stages, ciphertext feeds back into the top of the next block cipher"
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

    <!-- STAGE 2 (chains off stage 1 ciphertext) -->
    <v-click>
      <!-- feedback wire: STAGE 1 ciphertext -> top of STAGE 2 box -->
      <div class="fb w1-down"></div>
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
      <!-- feedback wire: STAGE 2 ciphertext -> top of STAGE 3 box -->
      <div class="fb w2-down"></div>
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
/* CFB geometry: native design space 780px wide x 210px tall
   (N native px = N/7.8 cqw horizontal, N/2.1 cqh vertical) */
.cfb .stage { height: 100cqh; }
.cfb .top-in { height: 20.95cqh; }
.cfb .box-row { height: 22.86cqh; }
.cfb .arrow-d { height: 9.52cqh; }
.cfb .xor-row { height: 15.24cqh; }
.cfb .out { height: 11.43cqh; line-height: 11.43cqh; }
.cfb .iv, .cfb .key, .cfb .plain, .cfb .out { font-size: 9.52cqh; }
.cfb .arrow-r { width: 3cqw; }
.cfb .xor { font-size: 10.48cqh; }
.cfb .box { width: 19cqw; height: 22.86cqh; font-size: 9.52cqh; }

/* feedback wire: down from ciphertext (y=188..208) at the source stage
   center, right to the boundary (x=260), up to the box-top level
   (y=44), right along the top to the target stage center, downward
   arrowhead into the box top. (wire k: +33.33cqw on every left) */
.cfb .w1-down  { left: 16.67cqw; top: 89.52cqh; width: 2px; height: 9.52cqh; }
.cfb .w1-right { left: 16.67cqw; top: 99.05cqh; width: 16.67cqw; height: 2px; }
.cfb .w1-up    { left: 33.33cqw; top: 5.71cqh;  width: 2px; height: 93.33cqh; }
.cfb .w1-top   { left: 33.33cqw; top: 5.71cqh;  width: 16.67cqw; height: 2px; }
.cfb .w1-drop  { left: 50cqw;    top: 5.71cqh;  width: 2px; height: 10.95cqh; }
.cfb .w1-head  { left: 50cqw;    top: 16.67cqh; }   /* point lands on the box border (y=44) */
.cfb .w2-down  { left: 50cqw;    top: 89.52cqh; width: 2px; height: 9.52cqh; }
.cfb .w2-right { left: 50cqw;    top: 99.05cqh; width: 16.67cqw; height: 2px; }
.cfb .w2-up    { left: 66.67cqw; top: 5.71cqh;  width: 2px; height: 93.33cqh; }
.cfb .w2-top   { left: 66.67cqw; top: 5.71cqh;  width: 16.67cqw; height: 2px; }
.cfb .w2-drop  { left: 83.33cqw; top: 5.71cqh;  width: 2px; height: 10.95cqh; }
.cfb .w2-head  { left: 83.33cqw; top: 16.67cqh; }
</style>
