(() => {
  const form = document.querySelector("[data-search-form]");
  const input = document.querySelector("[data-search-input]");
  const results = document.querySelector("[data-search-results]");
  const status = document.querySelector("[data-search-status]");

  if (!form || !input || !results) {
    return;
  }

  const endpoint =
    "https://blahblah-this-endpoint-nlweb.michal-piekarczyk.workers.dev/ask";

  const setStatus = (message, isError = false) => {
    if (!status) {
      return;
    }
    status.textContent = message;
    status.dataset.state = isError ? "error" : "info";
  };

  const clearResults = () => {
    results.innerHTML = "";
  };

  const renderResults = (payload) => {
    clearResults();
    if (!payload) {
      results.innerHTML = "<p>No results returned.</p>";
      return;
    }

    if (typeof payload === "string") {
      results.innerHTML = `<p>${payload}</p>`;
      return;
    }

    const summary =
      payload.answer || payload.summary || payload.response || payload.message;

    if (summary) {
      const summaryEl = document.createElement("div");
      summaryEl.className = "search-summary";
      summaryEl.textContent = summary;
      results.appendChild(summaryEl);
    }

    const items = payload.results || payload.pages || payload.items || [];

    if (Array.isArray(items) && items.length > 0) {
      const list = document.createElement("ul");
      list.className = "search-results";
      items.forEach((item) => {
        const entry = document.createElement("li");
        const schema = item.schema_object || {};
        const title =
          schema.name || item.title || item.name || item.slug || "Result";
        const url = item.url || item.permalink || item.link;
        const scoreText =
          typeof item.score === "number" ? ` (${item.score.toFixed(3)})` : "";

        const header = document.createElement("div");
        header.className = "search-result-header";

        if (url) {
          const link = document.createElement("a");
          link.href = url;
          link.textContent = `${title}${scoreText}`;
          header.appendChild(link);
        } else {
          header.textContent = `${title}${scoreText}`;
        }

        entry.appendChild(header);

        const description =
          schema.description || item.description || item.snippet || item.summary;
        if (description) {
          const snippet = document.createElement("p");
          snippet.textContent = description;
          entry.appendChild(snippet);
        }

        list.appendChild(entry);
      });
      results.appendChild(list);
    }

    if (!summary && (!Array.isArray(items) || items.length === 0)) {
      results.innerHTML = `<pre>${JSON.stringify(payload, null, 2)}</pre>`;
    }
  };

  const parseEventStream = (rawText) => {
    const summaryParts = [];
    let results = [];
    rawText
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line.startsWith("data:"))
      .forEach((line) => {
        const jsonText = line.replace(/^data:\s*/, "");
        if (!jsonText) {
          return;
        }
        try {
          const payload = JSON.parse(jsonText);
          if (payload.message_type === "summary" && payload.message) {
            summaryParts.push(payload.message);
          }
          if (
            payload.message_type === "result_batch" &&
            Array.isArray(payload.results)
          ) {
            results = payload.results;
          }
        } catch (error) {
          console.warn("Unable to parse search stream payload", error);
        }
      });

    return {
      summary: summaryParts.join("").trim(),
      results,
    };
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = input.value.trim();
    if (!query) {
      setStatus("Enter a search query.", true);
      return;
    }

    const params = new URLSearchParams({
      query,
      generate_mode: "summarize",
      display_mode: "full",
      site: "all",
    });

    setStatus("Searching...", false);
    clearResults();

    try {
      const response = await fetch(`${endpoint}?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const contentType = response.headers.get("content-type") || "";
      let payload;
      if (contentType.includes("application/json")) {
        payload = await response.json();
      } else {
        const rawText = await response.text();
        if (rawText.includes("message_type")) {
          const parsed = parseEventStream(rawText);
          payload = {
            summary: parsed.summary,
            results: parsed.results,
          };
        } else {
          payload = rawText;
        }
      }
      renderResults(payload);
      setStatus("Search complete.", false);
    } catch (error) {
      setStatus(`Search failed: ${error.message}`, true);
    }
  });
})();
