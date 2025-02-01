export type CoordinatedEvent = { clientX: number; clientY: number }

export class Coordinate {
	constructor(
		public x: number,
		public y: number
	) { }

	static fromElement(el: HTMLElement): Coordinate {
		const rect = el.getBoundingClientRect()
		const { scrollX, scrollY } = window
		return new Coordinate(
			rect.left + scrollX + rect.width / 2,
			rect.top + scrollY + rect.height / 2
		)
	}

	public toString(): string {
		return `(${this.x}, ${this.y})`
	}

	public distanceFromEvent({ clientX, clientY }: CoordinatedEvent): number {
		const { scrollX, scrollY } = window
		const dx = Math.abs(this.x - clientX - scrollX)
		const dy = Math.abs(this.y - clientY - scrollY)
		return Math.sqrt(dx * dx + dy * dy)
	}

	public distanceFromRect({ top, right, bottom, left }: DOMRect): number {
		// Find nearest x point
		let nx = -1
		if (this.x < left) {
			nx = left
		} else if (this.x > right) {
			nx = right
		}

		// Find nearest y point
		let ny = -1
		if (this.y < top) {
			ny = top
		} else if (this.y > bottom) {
			ny = bottom
		}

		// Seems like coordinate is inside the rectangle
		if (nx === -1 && ny === -1) {
			return 0
		}

		// Find max distance
		let dx = 0
		let dy = 0
		if (nx !== -1) {
			dx = Math.abs(this.x - nx)
		}
		if (dy !== -1) {
			dy = Math.abs(this.y - ny)
		}
		return Math.min(dx, dy)
	}
}

export class Rectangle {
	constructor(
		public top: number,
		public right: number,
		public bottom: number,
		public left: number,
	) {}

	static fromDOMRect({ top, right, bottom, left }: DOMRect): Rectangle {
		const { scrollX, scrollY } = window
		return new Rectangle(
			top + scrollY,
			right + scrollX,
			bottom + scrollY,
			left + scrollX
		)
	}

	public toString(): string {
		return `(${this.top}, ${this.right}, ${this.bottom}, ${this.left})`
	}

	public expandBy(dx: number, dy: number) {
		this.top -= dy
		this.right += dx
		this.bottom += dy
		this.left -= dx
	}

	public shrinkBy(dx: number, dy: number) {
		this.top += dy
		this.right -= dx
		this.bottom -= dy
		this.left += dx
	}

	public contains({ clientX, clientY }: CoordinatedEvent): boolean {
		const { scrollX, scrollY } = window
		return clientX + scrollX >= this.left &&
			clientX + scrollX <= this.right &&
			clientY + scrollY >= this.top &&
			clientY + scrollY <= this.bottom
	}
}
