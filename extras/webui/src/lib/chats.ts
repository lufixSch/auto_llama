import { generateId } from './utils/id';

export enum Roles {
	system = 'system',
	assistant = 'assistant',
	user = 'user'
}

export interface Message {
	role: Roles;
	content: string;
	branches: number[];
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
		this.branches.push({
			source: sourceBranch,
			messages: this.branches[sourceBranch].messages.slice(0, msgIndex + 1)
		});
		this.branches[branchId].messages.forEach((msgId) =>
			this.messages[msgId].branches.push(branchId)
		);
		return branchId;
	}

	newMessage(role: Roles, content: string, branch: number) {
		const id = generateId(8);
		const message: Message = { role, content, branches: [branch] };
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

	static fromJson(json: Chat): Chat {
		const chat = new Chat(json.character);
		chat.messages = json['messages'];
		chat.branches = json['branches'];
		return chat;
	}
}
