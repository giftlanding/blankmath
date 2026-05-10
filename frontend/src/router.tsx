import { createRootRoute, createRoute, createRouter, Outlet } from "@tanstack/react-router";
import { AppShell } from "./components/AppShell";
import { CatalogPage } from "./routes/CatalogPage";
import { WorksheetPage } from "./routes/WorksheetPage";

const rootRoute = createRootRoute({
  component: () => (
    <AppShell>
      <Outlet />
    </AppShell>
  ),
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: CatalogPage,
});

const worksheetRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/$worksheetId",
  component: WorksheetPage,
});

const routeTree = rootRoute.addChildren([indexRoute, worksheetRoute]);

export const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
