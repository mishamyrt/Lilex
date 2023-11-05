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
  }

  .variant {
    user-select: none;
    display: flex;
    flex-direction: column;
    flex: 1;
    align-items: center;
    border: 1px solid;
    border-color: var(--color-background-dimmed);
    margin-left: -1px;
    cursor: pointer;
    transition: border-color 0.2s ease-out;
  }

  .variant.selected {
    border: 1px solid var(--color-accent);
  }

  .preview {
    transition: color var(--transition-fast), font-weight var(--transition-fast);
    font-family: var(--font-family);
    font-size: 26px;
    color: var(--color-content);
  }

  .variant:hover .preview {
    font-weight: 700;
  }

  .variant.selected .preview {
    color: var(--color-accent);
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
  }
</style>
