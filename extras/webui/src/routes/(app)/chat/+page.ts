import type { CharacterIndex } from '$lib/characters.js';

export const prerender = false;

export async function load({ fetch }) {
	const res = await fetch(`/api/character`);
	if (!res.ok) {
		throw new Error('Character index not found!');
	}

	try {
		return {
			characters: (await res.json()) as CharacterIndex
		};
	} catch {
		throw new Error('Unable to load Chat!');
	}
}
