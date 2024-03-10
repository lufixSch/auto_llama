import type { Chat } from '$lib/chats.js';

export const prerender = false;
export const ssr = false;

export async function load({ fetch, params }) {
	try {
		return {
			chat: (await (await fetch(`/api/chat/${params.id}`)).json()) as Chat,
			id: params.id
		};
	} catch {
		throw new Error('Chat not found');
	}
}
