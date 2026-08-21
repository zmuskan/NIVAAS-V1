import { useState } from "react";
import { Outlet } from "react-router-dom";
import { Navbar } from "@/components/layout/navbar";
import { Sidebar } from "@/components/layout/sidebar";
import { Footer } from "@/components/layout/footer";

/**
 * RootLayout — the persistent application shell. Every route renders
 * inside <Outlet /> here, wrapped by the console chrome (navbar + sidebar)
 * and closed by the footer. This is the only layout in the foundation;
 * feature pages compose their content inside it, they don't redefine it.
 */
export function RootLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen flex-col bg-ink">
      <Navbar onToggleSidebar={() => setSidebarOpen((prev) => !prev)} />

      <div className="flex flex-1">
        <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        <div className="flex min-w-0 flex-1 flex-col">
          <main className="flex-1">
            <Outlet />
          </main>
          <Footer />
        </div>
      </div>
    </div>
  );
}
