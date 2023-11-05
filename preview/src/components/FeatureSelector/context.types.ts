import type { Readable, Writable } from 'svelte/store'

export type FeatureMap = Record<string, string>

export type FeatureStore = Writable<FeatureMap>

export type FeatureSetter = (symbols: string, code: string) => void

export interface FeatureContext {
  features: Readable<string[]>
  setFeature: FeatureSetter
}
