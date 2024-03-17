export function generateId(length = 5) {
	return Math.floor(
		Math.pow(16, length - 1) + Math.random() * (Math.pow(16, length) - Math.pow(16, length - 1))
	).toString(16);
}
