/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Role } from './Role';
import type { TextContent } from './TextContent';
/**
 * OpenAI message parameters
 */
export type OpenAIMessage = {
    role: Role;
    content: (string | Array<TextContent>);
    name?: (string | null);
};

