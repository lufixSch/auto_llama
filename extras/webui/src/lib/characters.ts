export enum ChatType {
	instruct = 'instruct',
	chat = 'chat'
}

export type CharacterIndex = { [key: string]: string };

export class Character {
	constructor(
		public name: string,
		public systemPrompt: string,
		public greeting: string,
		public chatType: ChatType = ChatType.instruct,
		public names: { system: string; assistant: string; user: string } = {
			system: 'system',
			assistant: 'assistant',
			user: 'user'
		}
	) {}
}
