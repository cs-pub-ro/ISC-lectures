<!--
  CtrDiagram.vue — Counter (CTR) mode diagram, pure HTML/CSS.

  Usage in slides:  <CtrDiagram />  or  <CtrDiagram width="660px" height="159px" />

  CTR per stage (matches the reference layout):
      [<Nonce, Counter+i>]    (top label, arrow down into the box;
                               Nonce red, Counter gold)
      key -> [block cipher]
             ↓  keystream
      plaintext -> ⊕
             ↓
        ciphertext
  No feedback: each counter value is used once, so the blocks are
  independent.

  Sizing: width/height props (default 780x188px = this mode's native
  design space). Shared style vocabulary from mode-base.css; the cq*
  geometry below is CTR-specific:

      y=0   .top-in    (44)   y=112 .xor-row   (32)
      y=44  .box-row   (48)   y=144 .arrow-d   (20)
      y=92  .arrow-d   (20)   y=164 .out       (24)
-->
<script setup>
defineProps({
  width:  { type: String, default: '780px' },
  height: { type: String, default: '188px' },
})
</script>

<template>
  <div
    class="mode-root ctr"
    role="img"
    aria-label="CTR: three independent stages, each counter block encrypted and XORed with plaintext"
    :style="{ width, height }"
  >

    <v-click>
      <div class="stage">
        <div class="top-in"><span class="ctr-lbl">&lt;<span class="nonce">Nonce</span>, <span class="ctr-c">Counter</span>&gt;</span><span class="arrow-d"></span></div>
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

    <v-click>
      <div class="stage">
        <div class="top-in"><span class="ctr-lbl">&lt;<span class="nonce">Nonce</span>, <span class="ctr-c">Counter+1</span>&gt;</span><span class="arrow-d"></span></div>
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

    <v-click>
      <div class="stage">
        <div class="top-in"><span class="ctr-lbl">&lt;<span class="nonce">Nonce</span>, <span class="ctr-c">Counter+2</span>&gt;</span><span class="arrow-d"></span></div>
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
/* CTR geometry: native design space 780px wide x 188px tall
   (N native px = N/7.8 cqw horizontal, N/1.88 cqh vertical) */
.ctr .stage { height: 100cqh; }
.ctr .top-in { height: 23.4cqh; }
.ctr .box-row { height: 25.53cqh; }
.ctr .arrow-d { height: 10.64cqh; }
.ctr .xor-row { height: 17.02cqh; }
.ctr .out { height: 12.77cqh; line-height: 12.77cqh; }
.ctr .key, .ctr .plain, .ctr .out { font-size: 10.64cqh; }
.ctr .arrow-r { width: 3cqw; }
.ctr .xor { font-size: 11.7cqh; }
.ctr .box { width: 19cqw; height: 25.53cqh; font-size: 10.64cqh; }

/* counter label: <Nonce, Counter+i> with colored parts */
.ctr .ctr-lbl { font-size: 10.64cqh; font-weight: 600; }
.ctr .nonce   { color: #cc0000; }
.ctr .ctr-c   { color: #d4a017; }
</style>
