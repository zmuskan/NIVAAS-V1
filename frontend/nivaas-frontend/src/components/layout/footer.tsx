import { LogoMark } from "@/components/layout/logo-mark";

const footerLinks = {
  Product: [
    { label: "Property search", href: "/search" },
    { label: "Ward analytics", href: "/analytics" },
    { label: "Recommendations", href: "/recommendations" },
  ],
  Company: [
    { label: "About", href: "/about" },
    { label: "Methodology", href: "/methodology" },
  ],
  Legal: [
    { label: "Privacy", href: "/privacy" },
    { label: "Terms", href: "/terms" },
  ],
};

export function Footer() {
  return (
    <footer className="border-t border-line-dark bg-ink">
      <div className="container py-14">
        <div className="grid grid-cols-2 gap-10 md:grid-cols-4">
          <div className="col-span-2 md:col-span-1">
            <LogoMark />
            <p className="mt-3 max-w-xs text-body-sm text-text-secondary">
              Ward-level rental intelligence for Bangalore, built on real transaction data.
            </p>
          </div>

          {Object.entries(footerLinks).map(([heading, links]) => (
            <div key={heading}>
              <p className="font-mono text-caption uppercase tracking-wider text-text-tertiary">
                {heading}
              </p>
              <ul className="mt-3 space-y-2">
                {links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      className="text-body-sm text-text-secondary transition-colors hover:text-text-primary"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 flex flex-col items-start justify-between gap-4 border-t border-line-dark pt-6 sm:flex-row sm:items-center">
          <p className="text-body-sm text-text-tertiary">
            © {new Date().getFullYear()} NIVAAS. Bengaluru, Karnataka.
          </p>
          <p className="font-mono text-caption text-text-tertiary">12.9716° N, 77.5946° E</p>
        </div>
      </div>
    </footer>
  );
}
