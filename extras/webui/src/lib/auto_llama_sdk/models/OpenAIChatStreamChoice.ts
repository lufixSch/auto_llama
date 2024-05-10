/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { auto_llama_api__models__openai__OpenAIChatStreamChoice__Message } from './auto_llama_api__models__openai__OpenAIChatStreamChoice__Message';
/**
 * OpenAI chat stream choice parameters
 */
export type OpenAIChatStreamChoice = {
    /**
     * **UNSUPORTED** (always set to 'length')
     */
    finish_reason?: ('stop' | 'length' | 'content_filter' | 'tool_calls' | null);
    index: number;
    /**
     * **UNSUPORTED**
     */
    logprobs?: (Record<string, any> | null);
    delta: auto_llama_api__models__openai__OpenAIChatStreamChoice__Message;
};

