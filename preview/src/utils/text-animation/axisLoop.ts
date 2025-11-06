import { wrapChars } from "./nodes";
import { applyAxisValue, FontAxis } from "./variants";

type AxisLoopConfig = {
	axis: FontAxis;
	min: number;
	max: number;
	distance?: number;
	duration?: number;
};

function loopAxisValue(
	from: number,
	to: number,
	timestamp: number,
	duration: number,
) {
	const isInverted = Math.floor(timestamp / duration) % 2 === 1;
	const delta = ((to - from) * (timestamp % duration)) / duration;
	if (!isInverted) {
		return to - delta;
	}
	return from + delta;
}

/**
 * Creates looped
 * @param el
 * @param config
 */
export function createAxisLoop(el: HTMLElement, config: AxisLoopConfig) {
	el.style.width = el.offsetWidth + el.offsetWidth * 0.1 + "px";
	el.style.height = el.offsetHeight + el.offsetWidth * 0.1 + "px";

	const elements = wrapChars(el, "span");
	const values = Array(elements.length);
	const duration = config.duration || 1000;
	const delta = duration / 4;

	function drawAnimationFrame(time: number = 0) {
		for (let i = 0; i < elements.length; i++) {
			values[i] = loopAxisValue(
				config.min,
				config.max,
				time - delta * i,
				duration,
			);
		}

		for (let i = 0; i < elements.length; i++) {
			applyAxisValue(elements[i], config.axis, values[i]);
		}
		requestAnimationFrame(drawAnimationFrame);
	}

	drawAnimationFrame();
}
