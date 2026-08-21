import { NavLink } from "react-router-dom";
import { Menu, Moon, Sun } from "lucide-react";
import { LogoMark } from "@/components/layout/logo-mark";
import { Button } from "@/components/ui/button";
import { useTheme } from "@/providers/theme-provider";
import { cn } from "@/lib/utils";

interface NavbarProps {
  onToggleSidebar?: () => void;
}

const primaryLinks = [
  { to: "/", label: "Overview" },
  { to: "/search", label: "Search" },
  { to: "/analytics", label: "Analytics" },
  { to: "/recommendations", label: "Recommendations" },
];

/**
 * Top-level navbar. Fixed, translucent-on-scroll console header.
 * Route destinations below are placeholders for the router shell — the
 * corresponding pages are out of scope for this session and are not built.
 */
export function Navbar({ onToggleSidebar }: NavbarProps) {
  const { theme, setTheme } = useTheme();

  return (
    <header className="sticky top-0 z-40 border-b border-line-dark bg-ink/80 backdrop-blur-md">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={onToggleSidebar}
            aria-label="Toggle navigation"
          >
            <Menu className="h-5 w-5" />
          </Button>
          <LogoMark />
        </div>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Primary">
          {primaryLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                cn(
                  "rounded-md px-3 py-2 text-sm font-medium text-text-secondary transition-colors duration-200",
                  "hover:text-text-primary hover:bg-white/[0.04]",
                  isActive && "text-text-primary bg-white/[0.06]",
                )
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            aria-label="Toggle theme"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          >
            {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
          <Button variant="secondary" size="sm" className="hidden sm:inline-flex">
            Sign in
          </Button>
          <Button variant="primary" size="sm">
            Get started
          </Button>
        </div>
      </div>
    </header>
  );
}
