<script lang="ts">
  import { onMount } from 'svelte'
  import { load, Font } from 'opentype.js'
  import { RangeSlider, Block } from '$components'
  import { renderGlyphs } from './render'
  import Glyph from './Glyph.svelte'

  const VARIANTS = ['Thin', 'Regular', 'Bold']

  const fonts: Font[] = []
  let selectedVariant = 1
  let loading = true

  let fontSize = 70
  let hovered = false

  let leaveTimeout: number

  $: height = fontSize + 30
  $: width = height * 1.3

  onMount(() => {
    const requests = VARIANTS.map(v => load(`./ttf/Lilex-${v}.ttf`))
    Promise.all(requests)
      .then(masters => {
        fonts.push(...masters)
        loading = false
      })
  })

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

  $: glyphs = loading || !(selectedVariant in fonts)
    ? []
    : renderGlyphs(fonts[selectedVariant])
</script>


{#if !loading}
<Block title="Glyphs" dark={true}>
  <svelte:fragment slot="toolbar">
    <RangeSlider bind:value={fontSize} min={50} max={150} />
    <ul class="variants">
      {#each VARIANTS as variant, i}
        <li class="variants-item">
          <button
            class:active="{selectedVariant === i}"
            on:click={() => { selectedVariant = i }}>
            {variant}
          </button>
        </li>
      {/each}
    </ul>
  </svelte:fragment>
  <div
    style:--glyph-width="{width}px"
    style:--glyph-height="{height}px"
    class="glyphs"
    class:hover={hovered}>
    {#each glyphs as glyph}
      <div class="glyph">
        <Glyph on:mouseenter={handleHover} on:mouseleave={handleLeave} {glyph} />
      </div>
    {/each}
  </div>
</Block>
{/if}

<style>
  .variants-item button {
    appearance: none;
    font-size: 15px;
    line-height: 15px;
    background-color: transparent;
    border: none;
    background-color: transparent;
    color: var(--color-content);
    font-family: "Lilex";
    border-radius: 16px;
    padding: 6px 15px 5px;
    cursor: pointer;
  }

  .variants-item button.active {
    pointer-events: none;
    background-color: var(--color-content);
    color: var(--color-background);
  }

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

  ul {
    list-style: none;
    display: flex;
    padding: 0;
    gap: 8px;
    margin: 0;
  }
</style>
