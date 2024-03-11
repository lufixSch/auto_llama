import { Chat } from '$lib/chats.js';

export const prerender = false;

export async function load({ fetch, params }) {
	const res = await fetch(`/api/chat/${params.id}`);
	if (!res.ok) {
		throw new Error('Chat not found');
	}

	try {
		return {
			chat: Chat.fromJson((await res.json()) as Chat),
			id: params.id
		};
	} catch {
		throw new Error('Unable to load Chat!');
	}
}
