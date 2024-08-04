<script lang="ts">
  import { onMount } from 'svelte'
  import { RangeSlider, Block, SegmentSelect } from '$components'
  import { renderGlyphs } from './render'
  import Glyph from './Glyph.svelte'
  import { loadFamily, FONT_STYLES, FONT_WEIGHTS, type FontMap, type FontWeight, type FontStyle } from './fonts'

  let fonts: FontMap = {} as FontMap
  let selectedWeight: FontWeight = 'Regular'
  let selectedStyle: FontStyle = 'Roman'

  let loading = true

  let fontSize = 70
  let hovered = false
  let scrolled = false

  let leaveTimeout: number

  $: height = fontSize + 30
  $: width = height * 1.3

  function handleHover () {
    hovered = true
    if (leaveTimeout) {
      window.clearTimeout(leaveTimeout)
    }
  }

  function handleLeave () {
    leaveTimeout = window.setTimeout(() => {
      hovered = false
    }, 500)
  }

  function handleScroll () {
    if (!scrolled) {
      scrolled = true
      setTimeout(() => {
        scrolled = false
      }, 300)
    }
  }

  onMount(() => {
    loadFamily('Lilex', './ttf')
      .then(masters => {
        fonts = masters
        loading = false
      })

    document.addEventListener('scroll', handleScroll)
    return () => {
      document.removeEventListener('scroll', handleScroll)
    }
  })

  $: glyphs = loading || !(selectedStyle in fonts && selectedWeight in fonts[selectedStyle])
    ? []
    : renderGlyphs(fonts[selectedStyle][selectedWeight])
</script>


{#if !loading}
<Block title="Glyphs" dark={true}>
  <svelte:fragment slot="toolbar">
    <div class="accessor">
      <RangeSlider bind:value={fontSize} min={50} max={150} />
      <SegmentSelect options={FONT_STYLES} bind:value={selectedStyle} />
    </div>
    <SegmentSelect options={FONT_WEIGHTS} bind:value={selectedWeight} />
  </svelte:fragment>
  <div
    style:--glyph-width="{width}px"
    style:--glyph-height="{height}px"
    class="glyphs"
    class:hover={!scrolled && hovered}>
    {#each glyphs as glyph}
      <div class="glyph">
        <Glyph on:mouseenter={handleHover} on:mouseleave={handleLeave} {glyph} />
      </div>
    {/each}
  </div>
</Block>
{/if}

<style>


  .glyphs {
    --card-padding: 16px;
    display: grid;
    grid-template-columns: repeat(auto-fill, var(--glyph-width));
    gap: 8px
  }

  .glyph {
    transition: opacity var(--transition-fast);
  }

  .glyphs.hover .glyph {
    opacity: 0.2;
  }

  .glyphs .glyph:hover {
    opacity: 1;
    transition: opacity 0s;
  }

  .accessor {
    display: flex;
    gap: var(--space-2xl);
  }
</style>
