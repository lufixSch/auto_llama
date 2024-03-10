import fs from 'fs';
import { DATA_PATH } from '$env/static/private';
import type { Chat } from '$lib/chats';

export function getBasePath() {
	return DATA_PATH + '/chats';
}

export function getPath(id: string) {
	return DATA_PATH + '/chats/chat-' + id + '.json';
}

export function readChat(id: string) {
	const chat = JSON.parse(fs.readFileSync(getPath(id), 'utf-8'));
	return chat;
}

export function overwriteChat(id: string, chat: Chat) {
	fs.writeFileSync(getPath(id), JSON.stringify(chat));
}

export function overwriteIndex(data: { [key: string]: string }) {
	fs.writeFileSync(getBasePath() + '/index.json', JSON.stringify(data));
}

export function getIndex() {
	// Read index and create file if not existing
	try {
		const indexData = JSON.parse(
			fs.readFileSync(getBasePath() + '/index.json', { encoding: 'utf-8' })
		);
		return indexData as { [key: string]: string };
	} catch {
		const indexData = {};
		fs.writeFileSync(getBasePath() + '/index.json', JSON.stringify(indexData), { flag: 'wx' });
		return indexData as { [key: string]: string };
	}
}
