import fs from 'fs';
import { json } from '@sveltejs/kit';
import { getBasePath, getIndex, getPath, overwriteIndex } from '$lib/server/chat.js';
import { Chat, Roles } from '$lib/chats.js';
import { generateId } from '$lib/utils/id';
import { building } from '$app/environment';

if (!building) {
	if (!fs.existsSync(getBasePath())) {
		fs.mkdirSync(getBasePath(), { recursive: true });
	}
}

/** List all existing chats */
export function GET() {
	return json(getIndex());
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
	const id = generateId(5);

	if (conf.firstMessage) {
		chat.newMessage(Roles.user, conf.firstMessage, 0);
	}

	const index = getIndex();
	index[id] = conf.description;
	overwriteIndex(index);

	fs.writeFileSync(getPath(id), JSON.stringify(chat), { flag: 'wx' });

	return json({ id, index });
}
