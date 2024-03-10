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
		return await (
			await fetch(`${apiBase}/chat`, {
				method: 'POST',
				body: JSON.stringify({ description, character, firstMessage })
			})
		).json();
	}

	static async overwriteChat(id: string, chat: Chat) {
		return await (
			await fetch(`${apiBase}/chat/${id}`, {
				method: 'PUT',
				body: JSON.stringify(chat)
			})
		).json();
	}
}
