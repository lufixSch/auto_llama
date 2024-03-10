import fs from 'fs';
import { json } from '@sveltejs/kit';

import { readChat, getPath, getIndex, overwriteIndex, overwriteChat } from '$lib/server/chat';
import type { Chat } from '$lib/chats.js';

/** Get the chat with the given ID */
export async function GET({ params }) {
	const { id } = params;
	return json(readChat(id));
}

/** Delele the chat with the given ID */
export async function DELETE({ params }) {
	const { id } = params;

	fs.unlinkSync(getPath(id));

	const index = getIndex();
	delete index[id];
	overwriteIndex(index);

	return json(index);
}

/** Update the chat with the given ID */
export async function PUT({ request, params }) {
	const { id } = params;

	const chat: Chat = await request.json();
	overwriteChat(id, chat);

	return json({ message: 'Chat updated' });
}
