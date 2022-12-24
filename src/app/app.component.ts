/**
 * Copyright (c) 2022 7thCode.(http://seventh-code.com/)
 * This software is released under the MIT License.
 * opensource.org/licenses/mit-license.php
 */

import {Component, OnInit} from '@angular/core';
import {AppService, IErrorObject} from "./app.service";

/**
 *
 **/
@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    public username: string = "";
    public password: string = "";
    public display_name: string = "";
    public progress: boolean = false;
    /**
     *
     **/
    constructor(public service: AppService) {

    }

    /**
     *
     **/
    public ngOnInit() {
        const token: string | null = localStorage.getItem('access_token');
        if (token) {
            this.service.setAccessToken(token);
            this.progress = true;
            this.service.self((error: IErrorObject, result: any): void => {
                if (!error) {
                    this.progress = false;
                    this.display_name = result.username;
                }
            });
        } else {

        }
    }

    /**
     * login
     **/
    public login() {
        this.progress = true;
        this.service.login(this.username, this.password, (error: IErrorObject, result: any): void => {
            if (!error) {
                this.service.setAccessToken(result.access_token);
                localStorage.setItem('access_token', result.access_token);
                this.service.self((error: IErrorObject, result: any): void => {
                    if (!error) {
                        this.progress = false;
                        this.display_name = result.username;
                    }
                });
            }
        });
    }

    /**
     * logout
     **/
    public logout() {
        this.progress = true;
        this.service.logout((error: IErrorObject, result: any): void => {
            if (!error) {
                this.progress = false;
                localStorage.removeItem('access_token');
                this.display_name = "";
            }
        });
    }

    /**
     * getSelf
     **/
    public getSelf() {
        this.progress = true;
        this.service.self((error: IErrorObject, result: any): void => {
            if (!error) {
                this.progress = false;
                this.display_name = result.username;
            }
        });
    }

    /**
     * renewToken
     **/
    public renewToken() {
        this.progress = true;
        this.service.renewToken((error: IErrorObject, result: any): void => {
            if (!error) {
                this.progress = false;
                this.service.setAccessToken(result.access_token);
                localStorage.setItem('access_token', result.access_token);
            }
        });
    }

}
