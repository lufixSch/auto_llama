import { defaultLLMParams, type LLMParams } from './llm';

export enum ChatType {
	instruct = 'instruct',
	chat = 'chat'
}

export type CharacterIndex = { [key: string]: string };

export class Character {
	constructor(
		public name: string,
		public instructPrompt: string,
		public greeting: string,
		public chatType: ChatType = ChatType.instruct,
		public names: { system: string; assistant: string; user: string } = {
			system: 'system',
			assistant: 'assistant',
			user: 'user'
		},
		public params: LLMParams = defaultLLMParams
	) {}

	static fromJson(data: Character & { systemPrompt: string }) {
		if (data.systemPrompt) {
			data.instructPrompt = data.systemPrompt;
		}

		return new Character(
			data.name,
			data.instructPrompt,
			data.greeting,
			data.chatType,
			data.names,
			data.params || defaultLLMParams
		);
	}

	static empty() {
		return new Character('', '', '');
	}
}
