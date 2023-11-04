import { getContext, setContext } from 'svelte'
import { derived, writable, type Readable } from 'svelte/store'
import type { FeatureContext, FeatureMap, FeatureSetter, FeatureStore } from './context.types'

const CONTEXT_KEY = 'features'

function extractFeatures (store: FeatureStore): Readable<string[]> {
  return derived(store, f => Object.values(f).filter(Boolean))
}

function createSetter (store: FeatureStore): FeatureSetter {
  return (symbols, code) => store.update((v) => ({
    ...v,
    [symbols]: code
  }))
}

export function createFeaturesContext (): FeatureContext {
  const featureMap = writable<FeatureMap>({})
  const features = extractFeatures(featureMap)
  const setFeature = createSetter(featureMap)

  return setContext(CONTEXT_KEY, {
    features,
    setFeature
  })
}

export function getFeaturesContext (): FeatureContext {
  return getContext(CONTEXT_KEY)
}
