<script lang="ts">
  import type { Glyph } from './render'

  export let glyph: Glyph

  function handleClick () {
    if (glyph.unicode === undefined) {
      return
    }
    console.log(glyph)
    navigator.clipboard.writeText(String.fromCharCode(glyph.unicode))
  }
</script>

<div
  role="button"
  tabindex="0"
  on:click={handleClick}
  on:keypress={handleClick}
  on:mouseenter
  on:mouseleave
  class:clickable={glyph.unicode !== undefined}
  class="glyph">
  <div class="path">
    {@html glyph.svg}
  </div>
  <span class="name">{glyph.name}</span>
</div>

<style lang="scss">
  // .glyph-container {
  //   opacity: 0.2;
  // }

  .path {
    display: flex;
    justify-content: center;

    :global(svg) {
      display: block;
      width: calc(var(--glyph-width) - (var(--card-padding) * 2));
      height: var(--glyph-height);
      fill: var(--color-content);
      overflow: visible;
    }
  }

  .glyph {
    background-color: var(--color-background-overlay);
    padding: calc(var(--glyph-height) / 3) 0 10px 0;
    border-radius: 4px;
    transition: opacity var(--transition-default);
    overflow: hidden;
  }

  .glyph.clickable {
    cursor: pointer;
  }

  .glyph:hover {
    position: relative;
    overflow: visible;
  }

  .name {
    color: var(--color-content);
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
