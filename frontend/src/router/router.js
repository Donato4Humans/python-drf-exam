import {createBrowserRouter, Navigate} from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import {AdminPage} from "../pages/admin/AdminPage";
import {AutoSalonPage} from "../pages/auto_salon/AutoSalonPage";
import {ListingsPage} from "../pages/listings/ListingsPage";
import {LoginPage} from "../pages/login/LoginPage";
import {SellerPage} from "../pages/sellers/SellerPage";


const router = createBrowserRouter([
    {
        path: '', element: <MainLayout/>,
        children: [
            {
                index: true, element: <Navigate to={'login'}/>
            },
            {
                path: 'login', element: <LoginPage/>
            }
        ],
    },
    {
        path: 'listing', element: <ListingsPage/>
    },
    {
        path: 'sellers', element: <SellerPage/>
    },
    {
        path: 'auto_salon', element: <AutoSalonPage/>
    },
    {
        path: 'admin', element: <AdminPage/>,

    }
]);

export {
    router
}