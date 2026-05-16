import { Link } from "@tanstack/react-router";
import { Calculator, MailPlus } from "lucide-react";
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
          <div className="header-actions">
            <a
              className="suggest-link"
              href="mailto:suggestions@blankmath.com?subject=Worksheet%20suggestion&body=Worksheet%20idea%3A%0A%0AGrade%20level%3A%0A%0AExample%20problem%3A"
            >
              <MailPlus aria-hidden="true" size={17} />
              Suggest a worksheet
            </a>
            <span className="worksheet-count">{worksheets.length} worksheet types</span>
          </div>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
