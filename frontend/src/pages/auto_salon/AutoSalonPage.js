import React from 'react';
import {ChatComponent} from "../../components/chat/ChatComponent";
import "./AutoSalonPage.css";


const AutoSalonPage = () => {
    return (
        <div className={'auto-salon-page'}>
            <h1>AutoSalon Page</h1>
            <div>
                <ChatComponent/>
            </div>
        </div>
    );
};

export {
    AutoSalonPage
};