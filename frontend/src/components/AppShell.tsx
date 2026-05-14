import { Link } from "@tanstack/react-router";
import { Calculator } from "lucide-react";
import { ReactNode } from "react";
import { worksheets } from "../worksheetDefinitions";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="app">
      <header className="site-header">
        <div className="site-header-inner">
          <Link to="/" className="brand" aria-label="Blankmath home">
            <span className="brand-mark">
              <Calculator aria-hidden="true" size={21} />
            </span>
            <span>
              <strong>Blankmath</strong>
              <small>Printable math practice</small>
            </span>
          </Link>
          <span className="worksheet-count">{worksheets.length} worksheet types</span>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
