import APIInterface from '$lib/api.js';
import { Character } from '$lib/characters.js';

export const prerender = false;

export async function load({ fetch, params }) {
	const apiInterface = new APIInterface(fetch);
	const chat = await apiInterface.getChat(params.id);
	const character =
		chat.character != 'none' ? await apiInterface.getCharacter(chat.character) : Character.empty();

	try {
		return {
			chat,
			character,
			id: params.id
		};
	} catch {
		throw new Error('Unable to load Chat!');
	}
}
