import APIInterface from '$lib/api.js';

export const prerender = false;

export async function load({ fetch }) {
	const api = new APIInterface(fetch);

	try {
		return {
			characters: await api.getCharacterIndex()
		};
	} catch {
		throw new Error('Unable to load Chat!');
	}
}
