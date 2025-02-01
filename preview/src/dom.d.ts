type TagName = keyof HTMLElementTagNameMap;

type HTMLElementProps<T extends TagName> = Partial<
	Omit<HTMLElementTagNameMap[T], "children">
>;
