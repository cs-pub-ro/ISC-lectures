<!--
  CbcDiagram.vue — Cipher Block Chaining (CBC) diagram, pure HTML/CSS.

  Usage in slides:  <CbcDiagram />  or  <CbcDiagram width="660px" height="210px" />

  Sizing
  - The component takes width/height props (default 780x248px, the
    "native" design size). The root is a CSS size container
    (container-type: size), so every internal coordinate is expressed
    in cqw/cqh — i.e. a percentage of the actual width/height:
        vertical:  N native px  ->  N / 248 * 100 cqh
        horizontal: N native px  ->  N / 780 * 100 cqw
    The diagram therefore scales proportionally from any width/height.
    (Note: calc() cannot divide length by length, which is why the
    cqw/cqh container-query units are used instead of scale factors.)
    Line thickness (2px) and arrowheads stay fixed px — that's line
    weight, not layout.

  Layout (native 780x248 design space)
  - root: horizontal flex row of 3 identical .stage columns (260 wide)
  - .stage: 228px-tall flex column; every child has a fixed height,
    so vertical positions are predictable (needed for the wires):

      y=0    .plain      (24)   y=84   .arrow-d   (28)
      y=24   .arrow-d    (28)   y=112  .cipher-row(64)
      y=52   .xor-row    (32)   y=176  .arrow-d   (28)
                                 y=204  .out       (24)

  - Feedback wire (ciphertext -> next XOR) is 4 absolutely-positioned
    divs (.fb .w{1,2}-*) anchored on the root. Each wire lives in the
    NEXT stage's <v-click>, so it only appears once the XOR it
    points at is visible.
  - The U+2295 glyph already contains the circle, so .xor has no CSS
    border (single line, not a double one).
-->
<script setup>
defineProps({
  width:  { type: String, default: '780px' },
  height: { type: String, default: '248px' },
})
</script>

<template>
  <div
    class="cbctest"
    role="img"
    aria-label="CBC: three chained block-cipher stages"
    :style="{ width, height }"
  >

    <!-- STAGE 1 (first block: uses IV) -->
    <v-click>
      <div class="stage">
        <div class="plain">plaintext</div>
        <div class="arrow-d"></div>
        <div class="xor-row">
          <span class="xor">&#8853;</span>           <!-- circled plus (XOR) -->
          <span class="iv-in">
            <span class="iv">IV</span>
            <span class="arrow-r"></span>
          </span>
        </div>
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

    <!-- STAGE 2 (chains off stage 1 ciphertext) -->
    <v-click>
      <!-- feedback wire: STAGE 1 ciphertext -> STAGE 2 XOR
           (appears with STAGE 2, so it never points at an invisible XOR) -->
      <div class="fb w1-down"></div>
      <div class="fb w1-right"></div>
      <div class="fb w1-up"></div>
      <div class="fb w1-xor"></div>
      <div class="stage">
        <div class="plain">plaintext</div>
        <div class="arrow-d"></div>
        <div class="xor-row">
          <span class="xor">&#8853;</span>
        </div>
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

    <!-- STAGE 3 (last block: no outgoing wire) -->
    <v-click>
      <!-- feedback wire: STAGE 2 ciphertext -> STAGE 3 XOR -->
      <div class="fb w2-down"></div>
      <div class="fb w2-right"></div>
      <div class="fb w2-up"></div>
      <div class="fb w2-xor"></div>
      <div class="stage">
        <div class="plain">plaintext</div>
        <div class="arrow-d"></div>
        <div class="xor-row">
          <span class="xor">&#8853;</span>
        </div>
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

<style scoped>
/* All values in cqw/cqh: 1cqw = 1% of container width, 1cqh = 1% of
   container height. Native design space: 780px wide x 248px tall, so
   N native px = N/7.8 cqw (horizontal) or N/2.48 cqh (vertical). */
.cbctest {
  container-type: size;
  position: relative;
  display: flex;
  margin: 0.8em auto;
}
.stage {
  position: relative;            /* anchor for the .fb-* wires */
  width: 33.33cqw;               /* 260 / 780 */
  height: 91.94cqh;              /* 228 / 248 */
  display: flex; flex-direction: column; align-items: center;
}

/* labels (green = plaintext, cyan = IV, purple = key, red = ciphertext) */
.plain { height: 9.68cqh; line-height: 9.68cqh; color: #0a8a0a; font-weight: 600; font-size: 8.06cqh; }
.out   { height: 9.68cqh; line-height: 9.68cqh; color: #b71c1c; font-weight: 600; font-size: 8.06cqh; }
.iv    { color: #29b6f6; font-weight: 600; font-size: 8.06cqh; }
.key   { color: #7b1fa2; font-weight: 600; font-size: 8.06cqh; margin-right: 8px; }

/* vertical arrow: line + downward head (line weight stays fixed px) */
.arrow-d { width: 2px; height: 11.29cqh; background: #000; position: relative; }
.arrow-d::after {
  content: ""; position: absolute; bottom: -1px; left: 50%; transform: translateX(-50%);
  border-left: 7px solid transparent; border-right: 7px solid transparent;
  border-top: 9px solid #000;
}
/* horizontal arrow: line + rightward head */
.arrow-r { width: 3cqw; height: 2px; background: #000; position: relative; align-self: center; }
.arrow-r::after {
  content: ""; position: absolute; right: -1px; top: 50%; transform: translateY(-50%);
  border-top: 7px solid transparent; border-bottom: 7px solid transparent;
  border-left: 9px solid #000;
}

/* XOR row: the XOR stays centered on the column's 50%; the [IV ->] group
   is anchored to its left in stage 1 only, so it can't push it off-center */
.xor-row {
  height: 12.9cqh;
  display: flex; align-items: center; justify-content: center; position: relative;
}
.iv-in {
  position: absolute; top: 50%; transform: translateY(-50%);
  right: calc(50% + 1.41cqw + 4px);  /* 11 native px = circle radius, + gap */
  display: flex; align-items: center;
}
/* the U+2295 glyph already contains a circle: no CSS border, single line */
.xor { font-size: 8.87cqh; line-height: 1; }

/* cipher row: [key ->] anchored left, [ block cipher ] centered on 50% */
.cipher-row { height: 25.81cqh; display: flex; align-items: center; justify-content: center; position: relative; }
.key-in {
  position: absolute; top: 50%; transform: translateY(-50%);
  right: calc(50% + 9.5cqw);     /* 9.5cqw = half of box width */
  display: flex; align-items: center;
}
.box {
  width: 19cqw; height: 20.16cqh;
  border: 2px solid #000;
  display: flex; align-items: center; justify-content: center;
  color: #0d47d4; font-weight: 700;
  font-size: 7.26cqh;
}

/* feedback wire: down from ciphertext (y=226..248), right to the stage
   boundary, up to the XOR's height (y=68), then a short rightward arrow
   into the next circle's left edge (y=67).
   Native coords for wire k use stage-k's x0 = (k-1)*260. */
.fb { position: absolute; background: #000; }

/* wire 1: from STAGE 1 (x0 = 0) to STAGE 2's XOR */
.w1-down  { left: 16.67cqw; top: 91.13cqh; width: 2px;  height: 8.87cqh; }
.w1-right { left: 16.67cqw; top: 99.19cqh; width: 16.67cqw; height: 2px; }
.w1-up    { left: 33.08cqw; top: 27.42cqh; width: 2px;  height: 72.58cqh; }
.w1-xor   { left: 33.08cqw; top: 27.02cqh; width: 15.26cqw; height: 2px; }

/* wire 2: from STAGE 2 (x0 = 260) to STAGE 3's XOR */
.w2-down  { left: 50cqw;     top: 91.13cqh; width: 2px;  height: 8.87cqh; }
.w2-right { left: 50cqw;     top: 99.19cqh; width: 16.67cqw; height: 2px; }
.w2-up    { left: 66.41cqw;  top: 27.42cqh; width: 2px;  height: 72.58cqh; }
.w2-xor   { left: 66.41cqw;  top: 27.02cqh; width: 15.26cqw; height: 2px; }

.w1-xor::after, .w2-xor::after { /* rightward arrowhead into the XOR */
  content: ""; position: absolute; right: -1px; top: 50%; transform: translateY(-50%);
  border-top: 7px solid transparent; border-bottom: 7px solid transparent;
  border-left: 9px solid #000;
}
</style>
