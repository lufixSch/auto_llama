import fs from 'fs';
import { json } from '@sveltejs/kit';
import { getBasePath, getIndex, getPath, overwriteIndex } from '$lib/server/character';
import { Character, ChatType } from '$lib/characters';
import { generateId } from '$lib/utils/id';
import { building } from '$app/environment';

if (!building) {
	if (!fs.existsSync(getBasePath())) {
		fs.mkdirSync(getBasePath(), { recursive: true });
	}
}

/** List all existing characters */
export function GET() {
	const characterIndex = JSON.parse(fs.readFileSync(`${getBasePath()}/index.json`, 'utf-8'));
	return json(characterIndex);
}

/** Update the character index */
export async function PUT({ request }) {
	overwriteIndex(await request.json());
	return json({ message: 'Character index updated successfully' });
}

/** Create a new character */
export async function POST({ request }) {
	const conf: {
		name: string;
		systemPrompt: string;
		greeting?: string;
		chatType?: ChatType;
		names?: { system: string; assistant: string; user: string };
	} = await request.json();

	const character = new Character(
		conf.name,
		conf.systemPrompt,
		conf.greeting || '',
		conf.chatType || ChatType.instruct,
		conf.names || { system: 'system', assistant: 'assistant', user: 'user' }
	);
	const id = generateId(5);

	const index = getIndex();
	index[id] = character.name;
	overwriteIndex(index);

	fs.writeFileSync(getPath(id), JSON.stringify(character), { flag: 'wx' });

	return json({ id, index });
}
