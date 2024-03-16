import { generateId } from '$lib/utils/id';
import type { Character } from './characters';

export enum Roles {
	system = 'system',
	assistant = 'assistant',
	user = 'user'
}

export type ChatIndex = { [key: string]: string };

export interface Message {
	role: Roles;
	content: string;
	branches: number[];
	branchStart: number[];
}

export class Chat {
	messages: { [key: string]: Message } = {};
	branches: { source: number | null; messages: string[] }[] = [{ source: null, messages: [] }];

	constructor(public character: string) {}

	getBranch(branch: number): { id: string; message: Message }[] {
		return this.branches[branch].messages.map((id) => ({ id, message: this.messages[id] }));
	}

	createBranch(sourceBranch: number, messageId: string) {
		const msgIndex = this.branches[sourceBranch].messages.findIndex((id) => id === messageId);
		const branchId = this.branches.length;

		this.messages[messageId].branchStart.push(branchId);

		this.branches.push({
			source: sourceBranch,
			messages: this.branches[sourceBranch].messages.slice(0, msgIndex + 1)
		});
		this.branches[branchId].messages.forEach((msgId) =>
			this.messages[msgId].branches.push(branchId)
		);

		return branchId;
	}

	getBranchPath(branch: number) {
		const path: number[] = [branch];
		let current: number | null = branch;
		while (current !== null) {
			path.push(current);
			current = this.branches[current].source;
		}

		return path;
	}

	getBranchSet(branch: number) {
		const set = new Set<number>();
		let current: number | null = branch;
		while (current !== null) {
			set.add(current);
			current = this.branches[current].source;
		}

		return set;
	}

	newMessage(role: Roles, content: string, branch: number) {
		const id = generateId(8);
		const message: Message = { role, content, branches: [branch], branchStart: [] };
		this.messages[id] = message;
		this.branches[branch].messages.push(id);
		return id;
	}

	deleteMessage(id: string) {
		const msg = this.messages[id];
		msg.branches.forEach(
			(branch) =>
				(this.branches[branch].messages = this.branches[branch].messages.filter((i) => i !== id))
		);
		delete this.messages[id];
		return msg;
	}

	/** Format chat messages for generating a response in 'instruct' mode */
	formatInstruct(branch: number, char: Character) {
		const msg = this.getBranch(branch).map(({ message }) => ({
			role: message.role,
			content: message.content
		}));

		if (char.greeting) {
			msg.unshift({ role: Roles.system, content: char.greeting });
		}

		if (char.systemPrompt) {
			msg.unshift({ role: Roles.system, content: char.systemPrompt });
		}

		return msg;
	}

	/** Format chat messages for generating a response in 'chat' mode */
	formatChat(branch: number, char: Character) {
		const msg = this.formatInstruct(branch, char);

		return msg.reduce(
			(chat, message) => `${chat}${char.names[message.role]}: ${message.content}\n`,
			''
		);
	}

	static fromJson(json: Chat): Chat {
		const chat = new Chat(json.character);
		chat.messages = json['messages'];
		chat.branches = json['branches'];
		return chat;
	}
}
