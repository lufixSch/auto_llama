import { type ChatIndex } from '$lib/chats.js';

export const prerender = false;

export async function load({ fetch }) {
	const res = await fetch(`/api/chat`);
	if (!res.ok) {
		throw new Error('Unable to load Chats');
	}

	try {
		return {
			chatIndex: (await res.json()) as ChatIndex
		};
	} catch {
		throw new Error('Unable to load Chat!');
	}
}
