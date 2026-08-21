import { createBrowserRouter } from "react-router-dom";

import Landing from "@/routes/landing";
import Questionnaire from "@/pages/Questionnaire";
import Recommendations from "@/pages/Recommendations";
import LocalityProfilePage from "@/pages/LocalityProfilePage";
import ExplorePage from "@/pages/ExplorePage";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Landing />,
    },

    {
        path: "/questionnaire",
        element: <Questionnaire />,
    },

    {
        path: "/recommendations",
        element: <Recommendations />,
    },

    {

    path: "/locality/:slug",
    element: <LocalityProfilePage />,

    },

    {
        path: "/explore",
        element: <ExplorePage />,
    },
]);
