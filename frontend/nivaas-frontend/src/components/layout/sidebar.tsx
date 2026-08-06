import { NavLink } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { LayoutGrid, Search, LineChart, Sparkles, Bookmark, Settings, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

interface SidebarItem {
  to: string;
  label: string;
  icon: typeof LayoutGrid;
}

const primaryItems: SidebarItem[] = [
  { to: "/", label: "Overview", icon: LayoutGrid },
  { to: "/search", label: "Property search", icon: Search },
  { to: "/analytics", label: "Ward analytics", icon: LineChart },
  { to: "/recommendations", label: "Recommendations", icon: Sparkles },
];

const secondaryItems: SidebarItem[] = [
  { to: "/saved", label: "Saved listings", icon: Bookmark },
  { to: "/settings", label: "Settings", icon: Settings },
];

/**
 * Sidebar — persistent on desktop (lg+), an overlay drawer on smaller
 * viewports. Route destinations correspond to the router shell only;
 * the pages themselves are intentionally not built in this session.
 */
export function Sidebar({ open, onClose }: SidebarProps) {
  return (
    <>
      {/* Desktop: static column */}
      <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:border-r lg:border-line-dark lg:bg-ink">
        <SidebarContent />
      </aside>

      {/* Mobile: animated overlay drawer */}
      <AnimatePresence>
        {open && (
          <>
            <motion.div
              key="scrim"
              className="fixed inset-0 z-40 bg-ink/60 backdrop-blur-sm lg:hidden"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={onClose}
              aria-hidden="true"
            />
            <motion.aside
              key="drawer"
              className="fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r border-line-dark bg-ink lg:hidden"
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            >
              <div className="flex justify-end p-3">
                <Button variant="ghost" size="icon" onClick={onClose} aria-label="Close navigation">
                  <X className="h-5 w-5" />
                </Button>
              </div>
              <SidebarContent onNavigate={onClose} />
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  );
}

function SidebarContent({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <div className="flex h-full flex-col justify-between px-3 py-6">
      <div className="space-y-6">
        <SidebarGroup label="Console" items={primaryItems} onNavigate={onNavigate} />
        <SidebarGroup label="Personal" items={secondaryItems} onNavigate={onNavigate} />
      </div>

      <div className="rounded-md border border-line-dark bg-ink-raised p-3">
        <p className="font-mono text-caption text-text-tertiary">DATA SOURCE</p>
        <p className="mt-1 text-body-sm text-text-secondary">
          BBMP ward boundaries · PostGIS listings index
        </p>
      </div>
    </div>
  );
}

function SidebarGroup({
  label,
  items,
  onNavigate,
}: {
  label: string;
  items: SidebarItem[];
  onNavigate?: () => void;
}) {
  return (
    <div>
      <p className="px-3 font-mono text-caption uppercase tracking-wider text-text-tertiary">
        {label}
      </p>
      <nav className="mt-2 flex flex-col gap-0.5" aria-label={label}>
        {items.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            onClick={onNavigate}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-2.5 rounded-md px-3 py-2 text-sm font-medium text-text-secondary",
                "transition-colors duration-200 hover:bg-white/[0.04] hover:text-text-primary",
                isActive && "bg-signal-500/10 text-signal-300",
              )
            }
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
