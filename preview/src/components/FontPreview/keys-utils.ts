export type KeyHandler = (e: KeyboardEvent) => void

export function handleKeys (e: KeyboardEvent, handlers: Record<string, KeyHandler>) {
  if (!(e.key in handlers)) return

  e.preventDefault()
  handlers[e.key](e)
}

export async function setCursor (node: HTMLTextAreaElement, position: number) {
  setTimeout(() => {
    node.selectionStart = node.selectionEnd = position
  }, 0)
}
