import type { Font } from 'opentype.js'

export interface Glyph {
  name: string
  svg: string,
  unicode?: number
}

export function renderGlyphs (font: Font) {
  const glyphs: Glyph[] = []
  const parentNode = document.createElement('div')
  const svgNode = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  parentNode.appendChild(svgNode)
  svgNode.setAttribute('viewBox', '0 0 162 71')
  for (let i = 0; i < font.glyphs.length; i++) {
    const glyph = font.glyphs.get(i)
    if (!glyph.name || glyph.name.endsWith('spacer')) {
      continue
    }
    const path = glyph.getPath(0, 0, 162)

    svgNode.innerHTML = path.toSVG(10)

    const pathNode = svgNode.children[0] as SVGPathElement
    pathNode.style.transform = 'translate(32px, 90px)'
    glyphs.push({
      name: glyph.name,
      svg: parentNode.innerHTML,
      unicode: glyph.unicode
    })
  }
  return glyphs
}
