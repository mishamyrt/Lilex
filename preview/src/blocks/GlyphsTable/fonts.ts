import { load, Font } from 'opentype.js'

export const FONT_WEIGHTS = ['Thin', 'Regular', 'Bold'] as const
export const FONT_STYLES = ['Roman', 'Italic'] as const

export type FontWeight = typeof FONT_WEIGHTS[number]
export type FontStyle = typeof FONT_STYLES[number]
export type FontMap = Record<FontStyle, Record<FontWeight, Font>>

type FontVariant = {
  font: Font
  weight: FontWeight
  style: FontStyle
}

function getFontName (
  family: string,
  style: FontStyle,
  weight: FontWeight
): string {
  if (style !== 'Roman' && weight === 'Regular') {
    return `${family}-${style}`
  }
  if (style === 'Roman') {
    return `${family}-${weight}`
  }
  return `${family}-${weight}${style}`
}

function getFontUrl (name: string, path: string): string {
  return `${path}/${name}.ttf`
}

async function loadVariant (
  familyName: string,
  weight: FontWeight,
  style: FontStyle,
  path: string
): Promise<FontVariant> {
  const name = getFontName(familyName, style, weight)
  const url = getFontUrl(name, path)
  const font = await load(url)
  return { font, weight, style }
}

export async function loadFamily (name: string, path: string): Promise<FontMap> {
  const requests = FONT_WEIGHTS.map(weight =>
    FONT_STYLES.map(style =>
      loadVariant(name, weight, style, path))
  ).flat()
  const fonts = await Promise.all(requests)
  const map = fonts.reduce<FontMap>((map, variant) => {
    if (!map[variant.style]) {
      map[variant.style] = {} as Record<FontWeight, Font>
    }
    map[variant.style][variant.weight] = variant.font
    return map
  }, {} as FontMap)
  return map
}
