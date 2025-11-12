type ElementTagName = keyof HTMLElementTagNameMap;

type CreatedElements<T extends ElementTagName> = Array<
	HTMLElementTagNameMap[T]
>;

function charElements<T extends ElementTagName>(
	input: string,
	elementType: T,
): CreatedElements<T> {
	const chars = Array(input.length);
	for (let i = 0; i < input.length; i++) {
		chars[i] = document.createElement<T>(elementType);
		chars[i].textContent = input[i];
		chars[i].classList.add("glyphNode");
	}
	return chars;
}

export function wrapChars<T extends ElementTagName>(
	el: HTMLElement,
	elementType: T,
): CreatedElements<T> {
	const result = [];
	const initialNodes = Array.from(el.childNodes);
	for (const node of initialNodes) {
		if (node.nodeType === Node.TEXT_NODE && node.textContent) {
			const content = node.textContent.trim();
			if (content === "") {
				continue;
			}
			const parent = node.parentNode as HTMLElement;
			const chars = charElements(content, elementType);
			chars.forEach((span) => parent.insertBefore(span, node));
			parent.removeChild(node);
			result.push(...chars);
		} else if (node.nodeType === Node.ELEMENT_NODE) {
			result.push(...wrapChars(node as HTMLElement, elementType));
		}
	}
	return result;
}

export function setProps(
	element: HTMLElement,
	props: Record<string, string | number | boolean>,
) {
	for (const [key, value] of Object.entries(props)) {
		element.style.setProperty(key, value.toString());
	}
}
