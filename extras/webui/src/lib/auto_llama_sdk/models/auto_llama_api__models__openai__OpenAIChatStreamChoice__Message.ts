/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OpenAIToolCall } from './OpenAIToolCall';
import type { Role } from './Role';
export type auto_llama_api__models__openai__OpenAIChatStreamChoice__Message = {
    role: Role;
    content?: (string | null);
    /**
     * **UNSUPORTED**
     */
    tool_calls?: Array<OpenAIToolCall>;
};

