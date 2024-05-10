/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { auto_llama_api__models__openai__OpenAIChatChoice__Message } from './auto_llama_api__models__openai__OpenAIChatChoice__Message';
/**
 * OpenAI chat choice parameters
 */
export type OpenAIChatChoice = {
    /**
     * **UNSUPORTED** (always set to 'length')
     */
    finish_reason?: ('stop' | 'length' | 'content_filter' | 'tool_calls' | null);
    index: number;
    /**
     * **UNSUPORTED**
     */
    logprobs?: (Record<string, any> | null);
    message: auto_llama_api__models__openai__OpenAIChatChoice__Message;
};

