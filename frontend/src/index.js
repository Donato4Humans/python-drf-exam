import ReactDOM from 'react-dom/client';
import {RouterProvider} from "react-router-dom";
import {HeaderComponent} from "./components/header/HeaderComponent";
import {FooterComponent} from "./components/footer/FooterComponent";

import "./app.css";
import {router} from "./router/router";


const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
       <div className={'chat-app'}>
           <HeaderComponent/>
           <RouterProvider router={router}/>
           <FooterComponent/>
       </div>
);