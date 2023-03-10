/**
 * Copyright (c) 2022 7thCode.(http://seventh-code.com/)
 * This software is released under the MIT License.
 * opensource.org/licenses/mit-license.php
 */

import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse, HttpHeaders} from "@angular/common/http";
import {retry} from "rxjs/operators";

export interface ErrorObject {
    code: number;
    message: string;
    tag: string;
    origin: any;
}

export type IErrorObject = ErrorObject | null;
export type Callback<T> = (error: IErrorObject, results: T | null) => void;

/**
 *
 **/
@Injectable({
    providedIn: 'root'
})
export class AppService {

    private loginOptions: any = null;
    private accessOptions: any = null;

    constructor(public http: HttpClient) {

        this.loginOptions = {
            headers: new HttpHeaders({
                "Content-Type": "application/x-www-form-urlencoded"
            }),
            withCredentials: true,
        };

    }

    /**
     *
     **/
    protected isNumber(value: number): boolean {
        return ((typeof value === 'number') && (isFinite(value)));
    };

    /**
     *
     **/
    private Error(code: number, message: string): any {
        return {code: code, message: message};
    }

    /**
     *
     **/
    public setAccessToken(access_token: string): void {
        this.accessOptions = {
            headers: new HttpHeaders({"Accept": "application/json; charset=utf-8", "Authorization": "Bearer " + access_token}),
        };
    }

    /**
     *
     **/
    public removeAccessToken(): void {
        this.accessOptions = {
            headers: new HttpHeaders({"Accept": "application/json; charset=utf-8", "Authorization": "Bearer "}),
        };
    }

    public create(username: string, password: string, callback: Callback<any>): void {
        this.http.post("/account/create", {username: username, password: password}, this.accessOptions).pipe(retry(3)).subscribe(
            {
                next: (result: any): void => {
                    if (this.isNumber(result.code)) {
                        if (result.code === 0) {
                            callback(null, result);
                        } else {
                            callback(this.Error(500, "A01121"), null);
                        }
                    } else {
                        callback(this.Error(500, "A01122"), null);
                    }
                },
                error: (error: HttpErrorResponse): void => {
                    callback(this.Error(500, "A01123"), null);
                },
                complete: () => {
                }
            }
        );
    }

    public update(user_id: string, update: any, callback: Callback<any>): void {
        this.http.put("/account/update", {user_id: user_id, update: update}, this.accessOptions).pipe(retry(3)).subscribe(
            {
                next: (result: any): void => {
                    if (this.isNumber(result.code)) {
                        if (result.code === 0) {
                            callback(null, result);
                        } else {
                            callback(this.Error(500, "A01121"), null);
                        }
                    } else {
                        callback(this.Error(500, "A01122"), null);
                    }
                },
                error: (error: HttpErrorResponse): void => {
                    callback(this.Error(500, "A01123"), null);
                },
                complete: () => {
                }
            }
        );
    }

    public delete(username: string, password: string, callback: Callback<any>): void {
        this.http.delete("/account/delete", this.accessOptions).pipe(retry(3)).subscribe(
            {
                next: (result: any): void => {
                    if (this.isNumber(result.code)) {
                        if (result.code === 0) {
                            callback(null, result);
                        } else {
                            callback(this.Error(500, "A01121"), null);
                        }
                    } else {
                        callback(this.Error(500, "A01122"), null);
                    }
                },
                error: (error: HttpErrorResponse): void => {
                    callback(this.Error(500, "A01123"), null);
                },
                complete: () => {
                }
            }
        );
    }

    public list(query: any, option: any, callback: Callback<any>): void {
        this.http.get("/account/list?query=" + encodeURIComponent(JSON.stringify(query)) + "&option=" + encodeURIComponent(JSON.stringify(option)),

             {headers: new HttpHeaders({"Accept": "application/json; charset=utf-8"})}

            ).pipe(retry(3)).subscribe(
            {
                next: (result: any): void => {
                    if (this.isNumber(result.code)) {
                        if (result.code === 0) {
                            callback(null, result.value);
                        } else {
                            callback(this.Error(500, "A00121"), null);
                        }
                    } else {
                        callback(this.Error(500, "A00121"), null);
                    }
                },
                error: (error: HttpErrorResponse): void => {
                    callback(this.Error(500, "A00122"), null);
                },
                complete: () => {
                }
            }
        );
    }

    /**
     *
     * @param username
     * @param password
     * @param callback
     */
    public login(username: string, password: string, callback: Callback<any>): void {
        this.http.post("/login", "username=" + username + "&password=" + password, this.loginOptions).pipe(retry(3)).subscribe(
            {
                next: (result: any): void => {
                    if (this.isNumber(result.code)) {
                        if (result.code === 0) {
                            callback(null, result);
                        } else {
                            callback(this.Error(500, "A00121"), null);
                        }
                    } else {
                        callback(this.Error(500, "A00121"), null);
                    }
                },
                error: (error: HttpErrorResponse): void => {
                    callback(this.Error(500, "A00122"), null);
                },
                complete: () => {
                }
            }
        );
    }

    /**
     * @param callback
     */
    public logout(callback: Callback<any>): void {
        this.http.delete("/logout", this.accessOptions).pipe(retry(3)).subscribe(
            {
                next: (result: any): void => {
                    if (this.isNumber(result.code)) {
                        if (result.code === 0) {
                            this.removeAccessToken();
                            callback(null, result.value);
                        } else {
                            callback(this.Error(500, "A00121"), null);
                        }
                    } else {
                        callback(this.Error(500, "A00121"), null);
                    }
                },
                error: (error: HttpErrorResponse): void => {
                    callback(this.Error(500, "A00122"), null);
                },
                complete: () => {
                }
            }
        );
    }

    /**
     * @param callback
     */
    public getToken(callback: Callback<any>): void {
        this.http.get("/get_token", this.accessOptions).pipe(retry(3)).subscribe(
            {
                next: (result: any): void => {
                    if (this.isNumber(result.code)) {
                        if (result.code === 0) {
                            callback(null, result);
                        } else {
                            callback(this.Error(500, "A00121"), null);
                        }
                    } else {
                        callback(this.Error(500, "A00121"), null);
                    }
                },
                error: (error: HttpErrorResponse): void => {
                    callback(this.Error(500, "A00122"), null);
                },
                complete: () => {
                }
            }
        );
    }

    /**
     * @param callback
     */
    public renewToken(callback: Callback<any>): void {
        this.http.get("/renew_token", this.accessOptions).pipe(retry(3)).subscribe(
            {
                next: (result: any): void => {
                    if (this.isNumber(result.code)) {
                        if (result.code === 0) {
                            callback(null, result);
                        } else {
                            callback(this.Error(500, "A00121"), null);
                        }
                    } else {
                        callback(this.Error(500, "A00121"), null);
                    }
                },
                error: (error: HttpErrorResponse): void => {
                    callback(this.Error(500, "A00122"), null);
                },
                complete: () => {
                }
            }
        );
    }

    /**
     * @param callback
     */
    public self(callback: Callback<any>): void {
        this.http.get("/self", this.accessOptions).pipe(retry(3)).subscribe(
            {
                next: (result: any): void => {
                    if (this.isNumber(result.code)) {
                        if (result.code === 0) {
                            callback(null, result);
                        } else {
                            callback(this.Error(500, "A00121"), null);
                        }
                    } else {
                        callback(this.Error(500, "A00121"), null);
                    }
                },
                error: (error: HttpErrorResponse): void => {
                    callback(this.Error(500, "A00122"), null);
                },
                complete: () => {
                }
            }
        );
    }

}
