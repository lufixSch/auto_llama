import type { Chat } from '$lib/chats';

const apiBase = '/api';

export default class APIInterface {
	static async getChat(id: string) {
		return (await (await fetch(`${apiBase}/chat/${id}`)).json()) as Chat;
	}

	static async createChat(
		character: string,
		description: string,
		firstMessage?: string
	): Promise<{ id: string; index: { [key: string]: string } }> {
		const res = await fetch(`${apiBase}/chat`, {
			method: 'POST',
			body: JSON.stringify({ description, character, firstMessage })
		});

		if (!res.ok) {
			throw new Error('Failed to create chat');
		}

		return await res.json();
	}

	static async overwriteChat(id: string, chat: Chat) {
		const res = await fetch(`${apiBase}/chat/${id}`, {
			method: 'PUT',
			body: JSON.stringify(chat)
		});

		if (!res.ok) {
			throw new Error('Failed to update chat');
		}

		return await res.json();
	}
}
