import { getChat } from '$lib/chats';

export async function load({ params }) {
	try {
		return {
			chat: getChat(params.id)
		};
	} catch {
		throw new Error('Chat not found');
	}
}
