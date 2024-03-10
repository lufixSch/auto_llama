export enum Roles {
	system = 'system',
	assistant = 'assistant',
	user = 'user'
}

export interface Message {
	role: Roles;
	content: string;
	branch?: string;
}

export class Chat {
	messages: Message[] = [];
	branches: { [key: string]: Message[] } = {};

	constructor(public character: string) {}
}
