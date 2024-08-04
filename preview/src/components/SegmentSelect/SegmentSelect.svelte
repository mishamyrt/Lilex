<script lang="ts">
  import { onMount } from 'svelte'

  export let options: Readonly<string[]>
  export let value: string

  onMount(() => {
    if (!value) {
      value = options[0]
    }
  })
</script>

<ul class="variants">
  {#each options as option}
    <li class="variants-item">
      <button
        class:active="{value === option}"
        on:click={() => { value = option }}>
        {option}
      </button>
    </li>
  {/each}
</ul>

<style lang="scss">
  .variants-item {
    button {
      appearance: none;
      font-size: 15px;
      line-height: 15px;
      background-color: transparent;
      border: none;
      background-color: transparent;
      color: var(--color-content);
      font-family: var(--font-family);
      border-radius: 16px;
      padding: 6px 15px 5px;
      cursor: pointer;
      transition: font-weight var(--transition-fast);

      &:hover {
        font-weight: 600;
      }

      &.active {
        pointer-events: none;
        background-color: var(--color-content);
        color: var(--color-background);
      }
    }
  }

  ul.variants {
    list-style: none;
    display: flex;
    padding: 0;
    gap: 8px;
    margin: 0;
  }
</style>
