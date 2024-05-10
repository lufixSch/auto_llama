/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Version } from '../models/Version';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class WelcomeService {
    /**
     * Root
     * Base route with status message
     * @returns Version Successful Response
     * @throws ApiError
     */
    public static rootGet(): CancelablePromise<Version> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/',
        });
    }
}
