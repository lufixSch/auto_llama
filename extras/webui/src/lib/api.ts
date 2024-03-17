import { Chat, type ChatIndex } from '$lib/chats';
import { Character, type CharacterIndex } from './characters';

const apiBase = '/api';
type FetchType = typeof fetch;
export default class APIInterface {
	public fetch = fetch;

	constructor(fetcher: FetchType | null = null) {
		if (fetcher) this.fetch = fetcher;
	}

	static new() {
		return new APIInterface();
	}

	async getChat(id: string) {
		const res = await this.fetch(`${apiBase}/chat/${id}`);

		if (!res.ok) {
			throw new Error(`Failed to get chat ${id}: ${res.statusText}`);
		}

		return Chat.fromJson(await res.json());
	}

	async createChat(
		character: string,
		description: string,
		firstMessage?: string
	): Promise<{ id: string; index: { [key: string]: string } }> {
		const res = await this.fetch(`${apiBase}/chat`, {
			method: 'POST',
			body: JSON.stringify({ description, character, firstMessage })
		});

		if (!res.ok) {
			throw new Error('Failed to create chat');
		}

		return await res.json();
	}

	async overwriteChat(id: string, chat: Chat) {
		const res = await this.fetch(`${apiBase}/chat/${id}`, {
			method: 'PUT',
			body: JSON.stringify(chat)
		});

		if (!res.ok) {
			throw new Error('Failed to update chat');
		}

		return await res.json();
	}

	async deleteChat(id: string) {
		const res = await this.fetch(`${apiBase}/chat/${id}`, {
			method: 'DELETE'
		});

		if (!res.ok) {
			throw new Error('Failed to delete chat');
		}
	}

	async getChatIndex() {
		const res = await this.fetch(`${apiBase}/chat`);

		if (!res.ok) {
			throw new Error('Failed to get chats');
		}

		return (await res.json()) as ChatIndex;
	}

	async overwriteChatIndex(index: ChatIndex) {
		const res = await this.fetch(`${apiBase}/chat`, {
			method: 'PUT',
			body: JSON.stringify(index)
		});

		if (!res.ok) {
			throw new Error('Failed to update chat index');
		}
	}

	async createCharacter(character: Character): Promise<{ id: string; index: CharacterIndex }> {
		const res = await this.fetch(`${apiBase}/character`, {
			method: 'POST',
			body: JSON.stringify(character)
		});

		if (!res.ok) {
			throw new Error('Failed to create character');
		}

		return await res.json();
	}

	async overwriteCharacter(id: string, character: Character) {
		const res = await this.fetch(`${apiBase}/character/${id}`, {
			method: 'PUT',
			body: JSON.stringify(character)
		});

		if (!res.ok) {
			throw new Error('Failed to update character');
		}
	}

	async deleteCharacter(id: string) {
		const res = await this.fetch(`${apiBase}/character/${id}`, {
			method: 'DELETE'
		});

		if (!res.ok) {
			throw new Error('Failed to delete character');
		}
	}

	async getCharacter(id: string) {
		const res = await this.fetch(`${apiBase}/character/${id}`);

		if (!res.ok) {
			throw new Error(`Failed to get character ${id}: ${res.statusText}`);
		}

		return Character.fromJson(await res.json());
	}

	async getCharacterIndex() {
		const res = await this.fetch(`${apiBase}/character`);

		if (!res.ok) {
			throw new Error('Failed to get characters');
		}

		return (await res.json()) as CharacterIndex;
	}
}
