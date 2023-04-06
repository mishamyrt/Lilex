<script lang="ts">
  import { load, Font } from 'opentype.js'
  import { onMount } from 'svelte'
  import { renderGlyphs } from '../utils/glyphs'
  import type { Glyph } from '../utils/glyphs'
  import RangeSlider from '../components/RangeSlider.svelte'
  import Toolbar from '../components/Toolbar.svelte'

  const VARIANTS = ['Thin', 'Regular', 'Bold']

  const fonts: Font[] = []
  let selectedVariant = 1
  let loading = true

  let fontSize = 70
  let hovered = false

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

  function handleHover (e: MouseEvent) {
    (e.target as HTMLDivElement).classList.add('hover')
    hovered = true
  }

  function handleClick (glyph: Glyph) {
    if (glyph.unicode === undefined) {
      return
    }
    navigator.clipboard.writeText(String.fromCharCode(glyph.unicode))
  }

  function handleLeave (e: MouseEvent) {
    hovered = false
  }

  $: glyphs = (() => {
    if (loading) {
      return []
    }
    return renderGlyphs(fonts[selectedVariant])
  })()
</script>

{#if !loading}
<div class="container">
  <h1>Glyphs</h1>
  <Toolbar>
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
  </Toolbar>
  <div
    style:--width="{width}px"
    style:--height="{height}px"
    class="glyphs"
    class:hover={hovered}>
    {#each glyphs as glyph}
      <div
        on:click={() => handleClick(glyph)}
        on:keypress={() => handleClick(glyph)}
        on:mouseenter={handleHover}
        on:mouseleave={handleLeave}
        class:clickable={glyph.unicode !== undefined}
        class="glyph-container">
        <div class="glyph-path">
          {@html glyph.svg}
        </div>
        <span class="glyph-name">{glyph.name}</span>
      </div>
    {/each}
  </div>
</div>
{/if}

<style>
  h1 {
    font-size: 7vw;
    font-weight: 200;
  }

  .container {
    --color-card-background: #282828;

    padding: var(--padding-layout);
  }

  .variants-item button {
    appearance: none;
    font-size: 15px;
    line-height: 15px;
    background-color: transparent;
    border: none;
    background-color: transparent;
    color: var(--color-text);
    font-family: "Lilex";
    border-radius: 16px;
    padding: 6px 15px 5px;
    cursor: pointer;
  }

  .variants-item button.active {
    pointer-events: none;
    background-color: var(--color-text);
    color: var(--color-background);
  }

  .glyphs {
    --card-padding: 16px;
    display: grid;
    grid-template-columns: repeat(auto-fill, var(--width));
    gap: 8px
  }

  .glyphs.hover .glyph-container {
    opacity: 0.2;
  }

  .glyph-path {
    display: flex;
    justify-content: center;
  }

  .glyph-path :global(svg) {
      display: block;
      width: calc(var(--width) - (var(--card-padding) * 2));
      height: var(--height);
      fill: var(--color-text);
      overflow: visible;
  }

  ul {
    list-style: none;
    display: flex;
    padding: 0;
    gap: 8px;
    margin: 0;
  }

  .glyph-container {
    background-color: var(--color-card-background);
    padding: calc(var(--height) / 3) 0 10px 0;
    border-radius: 4px;
    transition: opacity .3s ease-out;
    overflow: hidden;
  }

  .glyph-container.clickable {
    cursor: pointer;
  }

  .glyphs .glyph-container:hover {
    position: relative;
    overflow: visible;
    transition: opacity 0s;
    opacity: 1;
  }

  .glyph-name {
    font-size: 12px;
    display: block;
    text-align: center;
    text-overflow: ellipsis;
    line-height: 16px;
    overflow: hidden;
    width: 100%;
    margin-top: 12px;
    mix-blend-mode: exclusion;
  }
</style>
