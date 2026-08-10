import { createBrowserRouter } from "react-router-dom";

import Landing from "@/routes/landing";
import Questionnaire from "@/pages/Questionnaire";
import Recommendations from "@/pages/Recommendations";
import LocalityProfile from "@/pages/LocalityProfile";

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
        element: <LocalityProfile />,
    },
]);
