import { Link } from "@tanstack/react-router";
import { Calculator, Check, Copy } from "lucide-react";
import { ReactNode, useState } from "react";
import { worksheets } from "../worksheetDefinitions";

type AppShellProps = {
  children: ReactNode;
};

const suggestionEmail = "suggestions@blankmath.com";

export function AppShell({ children }: AppShellProps) {
  const [copiedSuggestionEmail, setCopiedSuggestionEmail] = useState(false);

  const copySuggestionEmail = async () => {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(suggestionEmail);
    } else {
      const textArea = document.createElement("textarea");
      textArea.value = suggestionEmail;
      textArea.style.position = "fixed";
      textArea.style.opacity = "0";
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
    }
    setCopiedSuggestionEmail(true);
    window.setTimeout(() => setCopiedSuggestionEmail(false), 1800);
  };

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
            <div className="suggest-email" aria-label="Suggest a worksheet by email">
              <span className="suggest-email-label">Suggest a worksheet</span>
              <span className="suggest-email-address">{suggestionEmail}</span>
              <button
                className="suggest-copy-button"
                type="button"
                onClick={copySuggestionEmail}
                aria-label={`Copy ${suggestionEmail}`}
                title={copiedSuggestionEmail ? "Copied" : "Copy email address"}
              >
                {copiedSuggestionEmail ? (
                  <Check aria-hidden="true" size={17} />
                ) : (
                  <Copy aria-hidden="true" size={17} />
                )}
              </button>
            </div>
            <span className="worksheet-count">{worksheets.length} worksheet types</span>
          </div>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
