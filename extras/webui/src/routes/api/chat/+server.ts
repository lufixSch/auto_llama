import fs from 'fs';
import { json } from '@sveltejs/kit';
import { getBasePath, getIndex, getPath, overwriteIndex } from '$lib/server/chat.js';
import { Chat, Roles } from '$lib/chats.js';

/** List all existing chats */
export function GET() {
	const chatIndex = JSON.parse(fs.readFileSync(`${getBasePath()}/index.json`, 'utf-8'));
	return json(chatIndex);
}

/** Update the chat index */
export async function PUT({ request }) {
	overwriteIndex(await request.json());
	return json({ message: 'Chat index updated successfully' });
}

/** Creaate a new chat */
export async function POST({ request }) {
	const conf: { description: string; character: string; firstMessage?: string } =
		await request.json();
	const chat = new Chat(conf.character);
	const id = Math.floor(Math.floor(100000 + Math.random() * 900000)).toString(16);

	if (conf.firstMessage) {
		chat.messages.push({ role: Roles.user, content: conf.firstMessage });
	}

	const index = getIndex();
	index[id] = conf.description;
	overwriteIndex(index);

	fs.writeFileSync(getPath(id), JSON.stringify(chat), { flag: 'wx' });

	return json({ id, index });
}
