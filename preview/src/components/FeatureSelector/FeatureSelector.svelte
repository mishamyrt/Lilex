<script lang="ts">
  import { createEventDispatcher, onDestroy, onMount } from 'svelte'
  import FeatureToggle from './FeatureToggle.svelte'
  import { createFeaturesContext } from './context'

  let unsubscribeFeatures: () => void

  const dispatch = createEventDispatcher()
  const { features } = createFeaturesContext()

  onMount(() => {
    unsubscribeFeatures = features.subscribe(value => {
      dispatch('change', value)
    })
  })

  onDestroy(() => {
    unsubscribeFeatures()
  })
</script>

<div class="container">
  <FeatureToggle title="Alt g" symbols="g" variants={['cv02', 'cv03']} />
  <FeatureToggle title="Alt zero" symbols="0" variants={['zero', 'cv04']} />
  <FeatureToggle title="Barless units" symbols="$¢" variants={['cv09']} />
  <FeatureToggle title="Alt arrows" symbols="↻" variants={['cv07']} />
  <FeatureToggle title="High asterisk" symbols="*" variants={['cv10']} />
  <FeatureToggle title="One storey a" symbols="a" variants={['cv01']} />
  <FeatureToggle title="Alt tilde" symbols="~" variants={['cv06']} />
  <FeatureToggle title="Alt eszett" symbols="ß" variants={['cv05', 'cv12']} />
  <FeatureToggle title="More arrows" symbols="<<=" variants={['ss01']} />
  <FeatureToggle title="Broken equals" symbols="!=" variants={['ss02']} />
  <FeatureToggle title="Alt equality" symbols=">=" variants={['cv08']} />
  <FeatureToggle title="Thin backslash" symbols="\\" variants={['ss03']} />
  <FeatureToggle title="Connected bar" symbols="|>" variants={['cv11']} />
  <FeatureToggle title="Broken #" symbols="##" variants={['ss04']} />
</div>

<style>
  .container {
    transition: background-color var(--transition-default);
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-s) var(--space-m);
  }
</style>
