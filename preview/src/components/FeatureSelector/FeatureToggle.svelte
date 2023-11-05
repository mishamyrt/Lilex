<script lang="ts">
  import FeatureVariant from './FeatureVariant.svelte'
  import { getFeaturesContext } from './context'

  export let title: string
  export let symbols: string
  export let variants: string[]

  let selected = ''

  const { setFeature } = getFeaturesContext()

  function setSelected (fea: string) {
    setFeature(symbols, fea)
    selected = fea
  }
</script>

<div class="toggle">
  <span class="title">{title}</span>
  <div class="variants">
    <FeatureVariant
      bind:symbols
      on:click={() => setSelected('')}
      selected={selected === ''}
      code="—"
    />
    {#each variants as fea}
      <FeatureVariant
        bind:symbols
        on:click={() => setSelected(fea)}
        selected={selected === fea}
        code={fea}
      />
    {/each}
  </div>
</div>

<style lang="scss">
  .variants {
    display: flex;
    background-color: var(--color-background-overlay);
    border-radius: 8px;
    padding: 4px;
  }

  .toggle {
    margin-bottom: 25px;
  }

  .title {
    color: var(--color-content-dimmed);
  }

  .title {
    font-size: 12px;
    display: block;
  }
</style>
