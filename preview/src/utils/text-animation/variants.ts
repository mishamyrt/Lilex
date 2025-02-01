export enum FontAxis {
  Weight = 'wght',
  Width = 'wdth',
  Slant = 'slnt',
  LowercaseHeight = 'YTLC'
}

export type VariationSettings = Partial<Record<FontAxis, number>>

export function formatVariation (axis: FontAxis, value: number) {
  return `"${axis}" ${value}`
}

export function formatVariations(
  settings: VariationSettings
): string {
  const props = Object.keys(settings) as (keyof VariationSettings)[]
  const params = Array(props.length)
  for (let i = 0; i < props.length; i++) {
    params[i] = formatVariation(props[i], settings[props[i]] as number)
  }
  return params.join(',')
}

export function applyVariants(
  el: HTMLElement,
  config: VariationSettings
) {
  el.style.fontVariationSettings = formatVariations(config)
}

export function applyAxisValue(el: HTMLElement, axis: FontAxis, value: number) {
  el.style.fontVariationSettings = formatVariation(axis, value)
}