export class Coordinate {
    public x: number
    public y: number

    constructor(x: number, y: number) {
        this.x = x
        this.y = y
    }

    static fromElement(el: HTMLElement): Coordinate {
        const rect = el.getBoundingClientRect()
        return new Coordinate(rect.left + rect.width / 2, rect.top + rect.height / 2)
    }

    static fromEvent(e: MouseEvent): Coordinate {
        return new Coordinate(e.clientX, e.clientY)
    }

    public toString(): string {
        return `(${this.x}, ${this.y})`
    }

    public distance(other: Coordinate): number {
        const dx = Math.abs(this.x - other.x)
        const dy = Math.abs(this.y - other.y)
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
