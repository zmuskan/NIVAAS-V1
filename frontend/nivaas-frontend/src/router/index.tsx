import { createBrowserRouter } from "react-router-dom";
import { RootLayout } from "@/layouts/root-layout";
import { RoutePlaceholder } from "@/routes/route-placeholder";
import { NotFoundRoute } from "@/routes/not-found";

/**
 * Application router.
 *
 * Every path here mirrors a link already rendered in the Navbar/Sidebar
 * so the shell can be navigated end-to-end. Each currently renders
 * <RoutePlaceholder /> — real feature pages (search, analytics,
 * recommendations, property detail) are explicitly out of scope for this
 * foundation session and will replace their placeholder in a future pass.
 */
export const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { index: true, element: <RoutePlaceholder routeName="Overview" /> },
      { path: "search", element: <RoutePlaceholder routeName="Property search" /> },
      { path: "analytics", element: <RoutePlaceholder routeName="Ward analytics" /> },
      { path: "recommendations", element: <RoutePlaceholder routeName="Recommendations" /> },
      { path: "saved", element: <RoutePlaceholder routeName="Saved listings" /> },
      { path: "settings", element: <RoutePlaceholder routeName="Settings" /> },
      { path: "*", element: <NotFoundRoute /> },
    ],
  },
]);
