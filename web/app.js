const state = {
	pop: 2000,
	compact: false,
	sel: new Map(),
	openCat: null,
};

const DATA = window.DATA;
const app = document.getElementById("app");

const esc = (s) =>
	String(s).replace(
		/[&<>"']/g,
		(c) =>
			({
				"&": "&amp;",
				"<": "&lt;",
				">": "&gt;",
				'"': "&quot;",
				"'": "&#39;",
			})[c],
	);

const fmt = (n, d = 0) =>
	n.toLocaleString("de-DE", {
		minimumFractionDigits: d,
		maximumFractionDigits: d,
	});

const dorf = (prozent) => (state.pop / 100) * prozent;

function progress(value, max, label) {
	const width = max > 0 ? Math.min(100, (value / max) * 100) : 0;
	return `<div class="progress"><div class="bar" style="width:${width.toFixed(2)}%"></div><span>${label}</span></div>`;
}

const dorfProgress = (prozent) => {
	const n = dorf(prozent);
	return progress(n, state.pop, fmt(n, 1));
};

function table(headers, rows) {
	const ths = headers.map((h) => `<th>${h}</th>`).join("");
	return `<div class="table-scroll"><table><thead><tr>${ths}</tr></thead><tbody>${rows.join("")}</tbody></table></div>`;
}

function header(title) {
	return `<h2>${esc(title)}</h2>`;
}

function renderAlleDaten() {
	const rows = DATA.data
		.slice()
		.sort(
			(a, b) =>
				a.Kategorie.localeCompare(b.Kategorie, "de") || b.Prozent - a.Prozent,
		)
		.map(
			(r) => `<tr>
        <td>${esc(r.Kategorie)}</td>
        <td>${esc(r.Titel)}</td>
        <td>${fmt(r.Personen)}</td>
        <td>${progress(r.Prozent, 100, `${fmt(r.Prozent, 2)} %`)}</td>
        <td>${fmt(dorf(r.Prozent), 1)}</td>
        <td>${r.Quelle ? `<a href="${esc(r.Quelle)}">Link</a>` : ""}</td>
        <td>${r.Jahr}</td>
        <td>${esc(r.Kommentar)}</td>
      </tr>`,
		);
	return (
		header("Alle Daten") +
		table(
			[
				"Kategorie",
				"Titel",
				"Personen",
				"Prozent",
				"Dorf",
				"Quelle",
				"Jahr",
				"Kommentar",
			],
			rows,
		)
	);
}

const categories = () => [...new Set(DATA.data.map((r) => r.Kategorie))];

function renderKategorien() {
	const cats = categories();
	const gridCols = state.compact ? "1fr 1fr" : "1fr";
	const blocks = cats
		.map((cat) => {
			const rows = DATA.data
				.filter((r) => r.Kategorie === cat)
				.sort(
					(a, b) =>
						dorf(b.Prozent) - dorf(a.Prozent) ||
						a.Titel.localeCompare(b.Titel, "de"),
				);
			const trs = rows.map(
				(r) =>
					`<tr><td>${esc(r.Titel)}</td><td>${dorfProgress(r.Prozent)}</td></tr>`,
			);
			return `<div class="block"><h3>${esc(cat)}</h3>${table(["Titel", "Dorf"], trs)}</div>`;
		})
		.join("");
	return (
		header("Kategorien") +
		`<label class="switch"><input type="checkbox" id="compact-toggle" ${state.compact ? "checked" : ""}> <span>kompaktes Layout</span></label>` +
		`<div class="grid kategorien" style="grid-template-columns:${gridCols}">${blocks}</div>`
	);
}

function renderEigeneTabelle() {
	const cols = state.compact ? 6 : 3;
	const groups = categories()
		.map((cat) => {
			const titles = DATA.data
				.filter((r) => r.Kategorie === cat)
				.map((r) => r.Titel)
				.sort((a, b) => a.localeCompare(b, "de"));
			const sel = state.sel.get(cat)?.size ?? 0;
			const options = titles
				.map(
					(t) =>
						`<label class="check"><input type="checkbox" class="titel-check" data-cat="${esc(cat)}" data-title="${esc(t)}" ${state.sel.get(cat)?.has(t) ? "checked" : ""}> ${esc(t)}</label>`,
				)
				.join("");
			const label = sel ? `${sel} ausgewählt` : "auswählen…";
			return `<div class="block"><h3>${esc(cat)}</h3><div class="multiselect${state.openCat === cat ? " open" : ""}" data-cat="${esc(cat)}"><button type="button" class="multiselect-toggle" aria-haspopup="true" aria-expanded="${state.openCat === cat}">${label}</button><div class="multiselect-menu">${options}</div></div></div>`;
		})
		.join("");

	const selRows = [];
	for (const [cat, titles] of state.sel) {
		for (const t of titles) {
			const r = DATA.data.find((d) => d.Kategorie === cat && d.Titel === t);
			if (r) selRows.push(r);
		}
	}
	selRows.sort(
		(a, b) =>
			dorf(b.Prozent) - dorf(a.Prozent) || a.Titel.localeCompare(b.Titel, "de"),
	);
	const tableHtml =
		header("Eigene Tabelle") +
		`<div class="grid" style="grid-template-columns:repeat(${cols}, 1fr)">${groups}</div>` +
		(selRows.length
			? table(
					["Titel", "Dorf"],
					selRows.map(
						(r) =>
							`<tr><td>${esc(r.Titel)}</td><td>${dorfProgress(r.Prozent)}</td></tr>`,
					),
				)
			: "");
	return tableHtml;
}

function renderWelt() {
	const dorfVonWelt = (einwohner) =>
		(einwohner / DATA.world_population) * state.pop;
	const row = (name, n) =>
		`<tr><td>${esc(name)}</td><td>${progress(n, state.pop, fmt(n, 0))}</td></tr>`;
	const continentRows = DATA.continents.map((c) =>
		row(c.Kontinent, dorfVonWelt(c.Einwohner)),
	);
	const countryRows = DATA.countries.map((c) =>
		row(c.Land, dorfVonWelt(c.Einwohner)),
	);
	return (
		header("Die Welt als Dorf") +
		`<p>Hier ist nun die ganze Weltbevölkerung auf das fiktive Dorf skaliert. Datenquelle: <a href="https://www.destatis.de/DE/Themen/Laender-Regionen/Internationales/Thema/Tabellen/Basistabelle_Bevoelkerung.html">2021</a></p>` +
		`<div class="grid kategorien"><div class="block"><h3>Aus Kontinent</h3>${table(["Kontinent", "Personen im Dorf"], continentRows)}</div><div class="block"><h3>Aus Land</h3>${table(["Land", "Personen im Dorf"], countryRows)}</div></div>`
	);
}

function renderFlaeche() {
	const rows = DATA.flaechennutzung.map((r) => {
		const prozent = `${fmt(r.Prozent, 2)} %`;
		return `<tr><td>${esc(r.Kategorie1)}</td><td>${esc(r.Kategorie2)}</td><td>${esc(r.Was)}</td><td>${fmt(r.qkm, 2)}</td><td>${progress(r.Prozent, 100, prozent)}</td></tr>`;
	});
	return (
		header("Flächennutzung") +
		`<p>Quelle: Daten großteils vom <a href="https://www-genesis.destatis.de/datenbank/online/statistic/33111/table/33111-0007/search/s/RmwlQzMlQTRjaGVubnV0enVuZw==">Destatis, 2023</a>, andere Quellen sind <a href="https://github.com/entorb/de-dorf/blob/main/data/flaechennutzung.tsv">hier</a> hinterlegt. Ergänzungen gerne direkt auf <a href="https://github.com/entorb/de-dorf/blob/main/data/flaechennutzung.tsv">GitHub</a> vorschlagen.</p>` +
		table(["Kategorie 1", "Kategorie 2", "Was", "qkm", "Prozent"], rows)
	);
}

function renderWeitereZahlen() {
	return `<div>${DATA.weitere_zahlen}</div>`;
}

function renderShell() {
	app.innerHTML = `
    <h1>Deutschland als Dorf</h1>
    <p>Um interessante Fakten zur deutschen Bevölkerung, wie beispielsweise "1.6 Mill. Millionäre", greifbarer zu machen, habe ich diese Zahlen auf ein Dorf mit 2000 Einwohnern umgerechnet. Das hilft mir, ein besseres Verständnis für die Welt außerhalb meiner eigenen sozialen Blase zu entwickeln. Das fiktive Dorf hätte dann 39 Millionäre, 41 geflüchtete Ukrainer und Syrer und 160 homo- oder bisexuelle Menschen.</p>
    <p>Viel Spaß damit wünscht Torben</p>
    <h2>Mitmachen</h2>
    <p>Hast Du weitere interessante Zahlen gefunden oder möchtest Aktualisierungen beisteuern? Dann schlag sie gerne direkt auf <a href="https://github.com/entorb/de-dorf/blob/main/data/data.tsv">GitHub</a> vor. Alternativ kannst Du auch über <a href="https://entorb.net/contact.php?origin=de-dorf">dieses Formular</a> Kontakt aufnehmen und Verbesserungsvorschläge einreichen.</p>

    <label class="pop-slider">Dorfbewohner: <input type="range" id="pop-slider" min="100" max="5000" step="25" value="${state.pop}"> <output id="pop-output">${state.pop}</output></label>

    <div id="data"></div>

    ${renderFlaeche()}
    ${renderWeitereZahlen()}
  `;
}

function render() {
	document.getElementById("data").innerHTML =
		`${renderAlleDaten()}${renderKategorien()}${renderEigeneTabelle()}${renderWelt()}`;
}

let popRaf = 0;
app.addEventListener("input", (e) => {
	if (e.target.id !== "pop-slider") return;
	state.pop = Number(e.target.value);
	document.getElementById("pop-output").textContent = state.pop;
	cancelAnimationFrame(popRaf);
	popRaf = requestAnimationFrame(render);
});

app.addEventListener("change", (e) => {
	if (e.target.id === "compact-toggle") {
		state.compact = e.target.checked;
		render();
	}
	if (e.target.classList.contains("titel-check")) {
		const cat = e.target.dataset.cat;
		const title = e.target.dataset.title;
		if (!state.sel.has(cat)) state.sel.set(cat, new Set());
		if (e.target.checked) {
			state.sel.get(cat).add(title);
		} else {
			state.sel.get(cat).delete(title);
			if (state.sel.get(cat).size === 0) state.sel.delete(cat);
		}
		render();
	}
});

app.addEventListener("click", (e) => {
	const toggle = e.target.closest(".multiselect-toggle");
	if (toggle) {
		const cat = toggle.closest(".multiselect").dataset.cat;
		state.openCat = state.openCat === cat ? null : cat;
		render();
	}
});

document.addEventListener("click", (e) => {
	if (state.openCat && !e.target.closest(".multiselect")) {
		state.openCat = null;
		render();
	}
});

document.addEventListener("keydown", (e) => {
	if (e.key === "Escape" && state.openCat) {
		state.openCat = null;
		render();
	}
});

renderShell();
render();
