import { Link } from "@tanstack/react-router";
import { ArrowRight, Search, SlidersHorizontal } from "lucide-react";
import { useMemo, useState } from "react";
import { worksheets } from "../worksheetDefinitions";

export function CatalogPage() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All");

  const categories = useMemo(() => ["All", ...Array.from(new Set(worksheets.map((item) => item.category)))], []);
  const filteredWorksheets = worksheets.filter((worksheet) => {
    const matchesCategory = category === "All" || worksheet.category === category;
    const haystack = `${worksheet.title} ${worksheet.category} ${worksheet.examples.join(" ")}`.toLowerCase();
    return matchesCategory && haystack.includes(query.trim().toLowerCase());
  });
  const totalControls = worksheets.reduce((sum, worksheet) => sum + worksheet.controls.length, 0);

  return (
    <section className="catalog">
      <div className="catalog-header">
        <div>
          <span className="section-kicker">Printable worksheet catalog</span>
          <h1>Build printable math practice sheets.</h1>
          <p>
            Arithmetic, comparison, math properties, and word-problem practice in one place.
          </p>
        </div>
        <div className="catalog-stats" aria-label="Catalog summary">
          <span>
            <strong>{worksheets.length}</strong>
            Worksheet types
          </span>
          <span>
            <strong>{categories.length - 1}</strong>
            Categories
          </span>
          <span>
            <strong>{totalControls}</strong>
            Options
          </span>
        </div>
      </div>

      <div className="catalog-toolbar">
        <label className="search-box">
          <Search aria-hidden="true" size={18} />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search worksheets"
            type="search"
          />
        </label>
        <div className="tabs" role="tablist" aria-label="Worksheet categories">
          {categories.map((item) => (
            <button
              key={item}
              className={item === category ? "active" : ""}
              onClick={() => setCategory(item)}
              type="button"
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      <div className="result-summary">
        <SlidersHorizontal aria-hidden="true" size={17} />
        <span>{filteredWorksheets.length} matching worksheet types</span>
      </div>

      <div className="worksheet-grid">
        {filteredWorksheets.map((worksheet) => (
          <article className="worksheet-card" key={worksheet.id}>
            <div>
              <span className="category-label">{worksheet.category}</span>
              <h2>{worksheet.title}</h2>
              <div className="card-examples" aria-label={`${worksheet.title} examples`}>
                {worksheet.examples.map((example) => (
                  <code key={example}>{example}</code>
                ))}
              </div>
            </div>
            <div className="card-footer">
              <span>{worksheet.controls.length} options</span>
              <Link to="/$worksheetId" params={{ worksheetId: worksheet.id }} className="primary-action">
                Configure <ArrowRight aria-hidden="true" size={16} />
              </Link>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
