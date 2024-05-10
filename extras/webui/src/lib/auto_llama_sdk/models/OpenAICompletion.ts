/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OpenAIResponseFormat } from './OpenAIResponseFormat';
/**
 * OpenAI completion parameters
 */
export type OpenAICompletion = {
    /**
     * **UNSUPORTED**
     */
    model?: string;
    /**
     * **UNSUPORTED**
     */
    frequency_penalty?: (number | null);
    /**
     * **UNSUPORTED**
     */
    logit_bias?: (Record<string, number> | null);
    /**
     * **UNSUPORTED**
     */
    logprobs?: (boolean | null);
    /**
     * **UNSUPORTED**
     */
    top_logprobs?: (number | null);
    max_tokens?: (number | null);
    /**
     * **UNSUPORTED**
     */
    'n'?: number;
    /**
     * **UNSUPORTED**
     */
    presence_penalty?: number;
    /**
     * **UNSUPORTED**
     */
    response_format?: (OpenAIResponseFormat | null);
    /**
     * **UNSUPORTED**
     */
    seed?: (number | null);
    stop?: (string | Array<string>);
    stream?: boolean;
    /**
     * **UNSUPORTED**
     */
    temperature?: number;
    /**
     * **UNSUPORTED**
     */
    top_p?: number;
    /**
     * **UNSUPORTED**
     */
    user?: string;
    prompt: (string | Array<string> | Array<number> | Array<Array<number>>);
    /**
     * **UNSUPORTED**
     */
    best_of?: number;
    /**
     * **UNSUPORTED**
     */
    echo?: boolean;
    /**
     * **UNSUPORTED**
     */
    suffix?: (string | null);
};

