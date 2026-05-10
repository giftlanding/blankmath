import { Link } from "@tanstack/react-router";
import { Search } from "lucide-react";
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

  return (
    <section className="catalog">
      <div className="catalog-header">
        <div>
          <h1>Worksheet Generator</h1>
          <p>Choose a worksheet type and configure printable practice sheets.</p>
        </div>
        <label className="search-box">
          <Search aria-hidden="true" size={18} />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search worksheets"
            type="search"
          />
        </label>
      </div>

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

      <div className="worksheet-grid">
        {filteredWorksheets.map((worksheet) => (
          <article className="worksheet-card" key={worksheet.id}>
            <div>
              <span className="category-label">{worksheet.category}</span>
              <h2>{worksheet.title}</h2>
              <p>{worksheet.examples.join("   ")}</p>
            </div>
            <Link to="/$worksheetId" params={{ worksheetId: worksheet.id }} className="primary-action">
              Generate
            </Link>
          </article>
        ))}
      </div>
    </section>
  );
}
