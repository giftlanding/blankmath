import { Link } from "@tanstack/react-router";
import { Calculator, Check, Copy, MailPlus } from "lucide-react";
import { ReactNode, useEffect, useRef, useState } from "react";
import { worksheets } from "../worksheetDefinitions";

type AppShellProps = {
  children: ReactNode;
};

const suggestionEmail = "suggestions@blankmath.com";

export function AppShell({ children }: AppShellProps) {
  const [suggestionsOpen, setSuggestionsOpen] = useState(false);
  const [copiedSuggestionEmail, setCopiedSuggestionEmail] = useState(false);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!suggestionsOpen) {
      return;
    }

    const closeOnOutsideClick = (event: PointerEvent) => {
      if (!suggestionsRef.current?.contains(event.target as Node)) {
        setSuggestionsOpen(false);
      }
    };

    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setSuggestionsOpen(false);
      }
    };

    document.addEventListener("pointerdown", closeOnOutsideClick);
    document.addEventListener("keydown", closeOnEscape);
    return () => {
      document.removeEventListener("pointerdown", closeOnOutsideClick);
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, [suggestionsOpen]);

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
            <div className="suggest-menu" ref={suggestionsRef}>
              <button
                className="suggest-button"
                type="button"
                onClick={() => setSuggestionsOpen((isOpen) => !isOpen)}
                aria-expanded={suggestionsOpen}
                aria-haspopup="dialog"
              >
                <MailPlus aria-hidden="true" size={17} />
                Suggest a worksheet
              </button>
              {suggestionsOpen ? (
                <div className="suggest-dropdown" role="dialog" aria-label="Suggest a worksheet by email">
                  <span className="suggest-dropdown-label">Email suggestions to</span>
                  <div className="suggest-email-row">
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
                </div>
              ) : null}
            </div>
            <span className="worksheet-count">{worksheets.length} worksheet types</span>
          </div>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
