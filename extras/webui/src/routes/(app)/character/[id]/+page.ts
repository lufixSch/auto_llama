import APIInterface from '$lib/api.js';

export const prerender = false;

export async function load({ fetch, params }) {
	const api = new APIInterface(fetch);

	try {
		return {
			character: await api.getCharacter(params.id),
			id: params.id
		};
	} catch {
		throw new Error('Unable to load Character!');
	}
}
