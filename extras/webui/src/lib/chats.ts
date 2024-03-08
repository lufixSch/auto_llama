import fs from 'fs';
import { DATA_PATH } from '$env/static/private';

export enum Roles {
	system,
	assistant,
	user
}

export interface Message {
	role: Roles;
	message: string;
	branch: string;
}

export class Chat {
	messages: Message[] = [];
	branches: { [key: string]: Message[] } = {};
	description: string = '';

	constructor(public character: string) {}
}

export function getChat(id: string) {
	return fs.readFileSync(DATA_PATH + `/chats/chat-${id}.json`).toJSON();
}

export function createChat(character: string) {
	const id = Math.floor(Math.floor(100000 + Math.random() * 900000)).toString(16);
	const chat = new Chat(character);

	fs.writeFileSync(DATA_PATH + `/chats/chat-${id}`, JSON.stringify(chat));

	return { id, chat };
}
