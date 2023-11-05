export const INDENT_SYMBOL = ' '
export const INDENT_SIZE = 2
export const INDENT = INDENT_SYMBOL.repeat(INDENT_SIZE)

export function lineOffsets (value: string, position: number) {
  const start = value.lastIndexOf('\n', position - 1) + 1
  const end = value.indexOf('\n', start)
  return { start, end }
}

export function indentLength (value: string, start: number, end: number) {
  let length = 0
  const line = value.substring(start, end).trim()
  for (let i = start; i < value.length; i++) {
    if (value[i] === INDENT_SYMBOL) {
      length++
    } else {
      break
    }
  }
  length = length / INDENT_SIZE
  const lastSymbol = line[line.length - 1]
  switch (lastSymbol) {
    case '{':
    case ':':
      length++
      break
  }
  return length
}

export function predictIndent (ref: HTMLTextAreaElement) {
  const value = ref.value
  const { start, end } = lineOffsets(value, ref.selectionStart)
  return indentLength(value, start, end)
}

export function formatIndent (size: number) {
  return INDENT.repeat(size)
}
