import React from 'react';
import {ChatComponent} from "../../components/chat/ChatComponent";
import "./SellerPage.css";


const SellerPage = () => {
    return (
        <div className={'seller-page'}>
            <h1>Seller Page</h1>
            <div>
                <ChatComponent/>
            </div>
        </div>
    );
};

export {
    SellerPage
};