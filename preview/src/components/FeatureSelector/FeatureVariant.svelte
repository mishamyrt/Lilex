<script lang="ts">
import { createEventDispatcher } from 'svelte'

export let selected: boolean
export let symbols: string
export let code: string

const dispatch = createEventDispatcher()

function emitClick () {
  dispatch('click')
}
</script>

<div
  on:click={emitClick}
  on:keypress={emitClick}
  class:selected
  class="variant"
  tabindex="0"
  role="button">
  <span style:font-feature-settings="'{code}'" class="preview">{symbols}</span>
  <span class="code">{code}</span>
</div>

<style>
  .code {
    color: var(--color-content-dimmed);
    position: absolute;
    bottom: -25px;
  }

  .variant {
    padding: 5px 0;
    user-select: none;
    display: flex;
    flex-direction: column;
    flex: 1;
    position: relative;
    align-items: center;
    font-weight: 300;
    border-radius: 4px;
    background-color: transparent;
    margin-left: -1px;
    cursor: pointer;
    transition: background-color var(--transition-fast), color var(--transition-fast);
  }

  .variant.selected {
    background-color: var(--color-background-overlay-active);
    cursor: default;
  }

  .preview {
    transition: color var(--transition-fast), font-weight var(--transition-fast);
    font-family: var(--font-family);
    font-size: 26px;
    color: var(--color-content);
    line-height: 1;
  }

  .variant:hover .preview {
    font-weight: 600;
  }

  .variant:first-child {
    margin: 0;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
  }

  .variant:last-child {
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
  }

  .code {
    font-size: 12px;
    font-weight: 400;
    color: var(--color-content-dimmed);
  }
</style>
