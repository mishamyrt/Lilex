type LayoutBlockVisibilityListener = (visible: boolean) => void

class LayoutBlockObserver {
	private observer: IntersectionObserver
	private callbacks: Record<string, LayoutBlockVisibilityListener[]> = {}

	constructor() {
		this.observer = new IntersectionObserver((entries) => {
			entries.forEach((entry) => {
				const block = entry.target as HTMLDivElement
				const name = block.getAttribute("data-block-name") || 'unknown'
				for (const callback of this.callbacks[name]) {
					callback(entry.isIntersecting)
				}
			})
		})

	const blocks = document.querySelectorAll<HTMLElement>(".block")
	blocks.forEach((block) => {
		const name = block.getAttribute("data-block-name") || 'unknown'
		this.callbacks[name] = []
		this.observer.observe(block)
	})
}

	public addVisibilityListener(name: string, listener: LayoutBlockVisibilityListener) {
		if (!this.callbacks[name]) {
			throw new Error(`Unknown block: ${name}`)
		}
		this.callbacks[name].push(listener)
	}
}

export const blocksObserver = new LayoutBlockObserver()
