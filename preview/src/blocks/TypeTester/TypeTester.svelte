<script lang="ts">
  import { RangeSlider, SchemeSelect, FeatureSelector, FontPreview, Block } from '$components'
  import { isDark } from '$utils'
  import { INITIAL_TEXT, MAX_WEIGHT, MIN_WEIGHT } from './constants'

  const weightDiff = MAX_WEIGHT - MIN_WEIGHT

  let value = INITIAL_TEXT
  let weight = 400
  let dark = isDark()
  let size = 70
  let features: string[] = []

  function handleMouseMove (e: MouseEvent) {
    const position = e.clientX
    const percent = position / window.innerWidth
    weight = (percent * weightDiff) + MIN_WEIGHT
  }

  function handleFeaturesChange (e: CustomEvent<string[]>) {
    features = e.detail
  }
</script>

<Block on:mousemove={handleMouseMove} bind:dark>
  <svelte:fragment slot="toolbar">
    <div class="left-accessor">
      <RangeSlider bind:value={size} min={12} max={200} />
      <span class="weight">{weight.toFixed(0)}</span>
    </div>
    <SchemeSelect bind:dark />
  </svelte:fragment>
  <div class="layout">
    <div class="preview">
      <FontPreview {weight} {size} {features} bind:value />
    </div>
    <div class="sidebar">
      <div class="feature-wrapper">
        <FeatureSelector on:change={handleFeaturesChange} />
      </div>

    </div>
  </div>
</Block>

<style>
  .layout {
    display: grid;
    grid-template-columns: 1fr 290px;
    gap: var(--padding-layout);
  }

  .feature-wrapper {
    position: sticky;
    top: 48px;
    max-height: calc(100vh - 55px);
    overflow-y: auto;
  }

  .left-accessor {
    display: flex;
    gap: var(--space-2xl);
  }

  .weight {
    font-family: var(--font-family);
    color: var(--color-content-dimmed);
  }
</style>
