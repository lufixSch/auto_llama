import APIInterface from '$lib/api';
import { redirect } from '@sveltejs/kit';
import auth from '$lib/auth';

export const prerender = false;
export const ssr = false;

export async function load({ fetch, params, url }) {
	// Check if the user is authenticated
	if (!auth.isAuthenticated) {
		return redirect(307, '/login');
	}

	const location = url.pathname.includes('chat') ? 'chat' : 'character';
	const apiInterface = new APIInterface(fetch);

	if (location === 'chat') {
		const chatIndex = await apiInterface.getChatIndex();

		if (params.id) {
			const chat = await apiInterface.getChat(params.id);

			if (chat.character != 'none') {
				const character = await apiInterface.getCharacter(chat.character);

				return { location, chatIndex, currentChar: { id: chat.character, name: character.name } };
			}
		}

		return { location, chatIndex };
	}

	if (location === 'character') {
		const charIndex = await apiInterface.getCharacterIndex();

		return { location, charIndex };
	}

	return {
		location
	};
}
