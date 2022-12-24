/**
 * Copyright (c) 2019 7thCode.(http://seventh-code.com/)
 * This software is released under the MIT License.
 * opensource.org/licenses/mit-license.php
 */

import {Component, OnInit} from '@angular/core';
import {AppService} from "./app.service";

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    logged_in: boolean = false;
    username: string = "";
    password: string = "";
    displayname: string = "";

    constructor(public service: AppService) {

    }

    /*
    * */
    public ngOnInit() {
        const token: string | null = localStorage.getItem('access_token');
        if (token) {
            this.service.setAccessToken(token);
            this.logged_in = true;
        } else {

        }
    }

    /*
    * */
    public login() {
        const username: string = "manager@gmail.com";
        const password: string = "id";
        this.service.login(username, password, (error, result) => {
            this.service.setAccessToken(result.access_token);
            localStorage.setItem('access_token', result.access_token);
            this.logged_in = true;
        });
    }

    /*
    * */
    public logout() {
        this.service.logout(() => {
            localStorage.removeItem('access_token');
            this.logged_in = false;
        });
    }

    /*
    * */
    public getSelf() {
        this.service.self((error, result) => {
            this.displayname = result.username
        });
    }

    /*
    * */
    public renewToken() {
        this.service.renewToken((error, result) => {
            this.service.setAccessToken(result.access_token);
            localStorage.setItem('access_token', result.access_token);
        });
    }

}
