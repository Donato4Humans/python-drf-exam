import React from 'react';
import {ChatComponent} from "../../components/chat/ChatComponent";
import "./ListingsPage.css";


const ListingsPage = () => {
    return (
        <div className={'listings-page'}>
            <h1>Listings Page</h1>
            <div>
                <ChatComponent/>
            </div>
        </div>
    );
};

export {
    ListingsPage
};