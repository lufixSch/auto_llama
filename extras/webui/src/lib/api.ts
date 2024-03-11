import { Chat, type ChatIndex } from '$lib/chats';

const apiBase = '/api';

export default class APIInterface {
	static async getChat(id: string) {
		const res = await fetch(`${apiBase}/chat/${id}`);

		if (!res.ok) {
			throw new Error(`Failed to get chat ${id}: ${res.statusText}`);
		}

		return Chat.fromJson(await res.json());
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

	static async deleteChat(id: string) {
		const res = await fetch(`${apiBase}/chat/${id}`, {
			method: 'DELETE'
		});

		if (!res.ok) {
			throw new Error('Failed to delete chat');
		}
	}

	static async getChatIndex() {
		const res = await fetch(`${apiBase}/chat`);

		if (!res.ok) {
			throw new Error('Failed to get chats');
		}

		return (await res.json()) as ChatIndex;
	}

	static async overwriteChatIndex(index: ChatIndex) {
		const res = await fetch(`${apiBase}/chat`, {
			method: 'PUT',
			body: JSON.stringify(index)
		});

		if (!res.ok) {
			throw new Error('Failed to update chat index');
		}
	}
}
