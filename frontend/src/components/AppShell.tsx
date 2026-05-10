import { Link } from "@tanstack/react-router";
import { ReactNode } from "react";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="app">
      <header className="site-header">
        <Link to="/" className="brand" aria-label="Blankmath home">
          <span className="brand-mark">B</span>
          <span>
            <strong>Blankmath</strong>
            <small>Unlimited FREE math worksheets</small>
          </span>
        </Link>
      </header>
      <main>{children}</main>
    </div>
  );
}
