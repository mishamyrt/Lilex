/**
 * Check if the browser is Safari
 */
export function checkIsSafari(): boolean {
	return (
		Boolean(navigator.userAgent.match(/safari/i)) &&
		!navigator.userAgent.match(/chrome/i) &&
		typeof document.body.style.webkitFilter === "string" &&
		!("chrome" in window)
	);
}
