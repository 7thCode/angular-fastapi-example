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
    public logged_in: boolean = false;
    public username: string = "";
    public password: string = "";
    public displayname: string = "";

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
            this.logged_in = true;
        } else {

        }
    }

    /**
     * login
     **/
    public login() {
        this.service.login(this.username, this.password, (error: IErrorObject, result: any): void => {
            if (!error) {
                this.service.setAccessToken(result.access_token);
                localStorage.setItem('access_token', result.access_token);
                this.logged_in = true;
            }
        });
    }

    /**
     * logout
     **/
    public logout() {
        this.service.logout((error: IErrorObject, result: any): void => {
            if (!error) {
                localStorage.removeItem('access_token');
                this.logged_in = false;
            }
        });
    }

    /**
     * getSelf
     **/
    public getSelf() {
        this.service.self((error: IErrorObject, result: any): void => {
            if (!error) {
                this.displayname = result.username;
            }
        });
    }

    /**
     * renewToken
     **/
    public renewToken() {
        this.service.renewToken((error: IErrorObject, result: any): void => {
            if (!error) {
                this.service.setAccessToken(result.access_token);
                localStorage.setItem('access_token', result.access_token);
            }
        });
    }

}
