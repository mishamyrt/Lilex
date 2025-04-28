import { atom } from 'nanostores'

export const $isGlyphsItalicEnabled = atom(false)

export function setGlyphsItalicEnabled(enabled: boolean) {
	console.log('setGlyphsItalicEnabled', enabled)
  $isGlyphsItalicEnabled.set(enabled);
}

export const $glyphsWeight = atom(400);

export function setGlyphsWeight(weight: number) {
	console.log('setGlyphsWeight', weight)
	$glyphsWeight.set(weight);
}
