import { Character } from '$lib/characters.js';

export const prerender = false;

export async function load({ fetch, params }) {
	const res = await fetch(`/api/character/${params.id}`);
	if (!res.ok) {
		throw new Error('Chat not found');
	}

	try {
		return {
			character: Character.fromJson((await res.json()) as Character),
			id: params.id
		};
	} catch {
		throw new Error('Unable to load Character!');
	}
}
