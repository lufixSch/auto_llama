import fs from 'fs';
import { error, json } from '@sveltejs/kit';

import {
	readCharacter,
	getPath,
	getIndex,
	overwriteIndex,
	overwriteCharacter
} from '$lib/server/character';
import type { Character } from '$lib/characters';

/** Get the character with the given ID */
export async function GET({ params }) {
	const { id } = params;

	try {
		return json(readCharacter(id));
	} catch {
		return error(404, 'Character not found!');
	}
}

/** Delete the character with the given ID */
export async function DELETE({ params }) {
	const { id } = params;

	fs.unlinkSync(getPath(id));

	const index = getIndex();
	delete index[id];
	overwriteIndex(index);

	return json(index);
}

/** Update the character with the given ID */
export async function PUT({ request, params }) {
	const { id } = params;

	const character: Character = await request.json();
	overwriteCharacter(id, character);

	return json({ message: 'Character updated' });
}
