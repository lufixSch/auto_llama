import APIInterface from '$lib/api.js';
import { Character } from '$lib/characters.js';

export const prerender = false;
export const ssr = false;

export async function load({ fetch, params, url }) {
	const apiInterface = new APIInterface(fetch);
	const chat = await apiInterface.getChat(params.id);
	const character =
		chat.character != 'none' ? await apiInterface.getCharacter(chat.character) : Character.empty();

	try {
		return {
			chat,
			character,
			id: params.id,
			branch: Number(url.searchParams.get('branch') || 0),
			new: url.searchParams.has('new')
		};
	} catch {
		throw new Error('Unable to load Chat!');
	}
}
