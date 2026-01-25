const $ = (id) => document.getElementById(id);

const createName = $("createName");
const createBody = $("createBody");
const readName = $("readName");
const readOutput = $("readOutput");
const notesList = $("notesList");
const searchNotes = $("searchNotes");
const notesCount = $("notesCount");

const btnCreate = $("btnCreate");
const btnRead = $("btnRead");
const btnRefresh = $("btnRefresh");
const btnClear = $("btnClear");
const btnCopy = $("btnCopy");
const btnCreateFill = $("btnCreateFill");

const toast = $("toast");

function showToast(msg, ok = true) {
    toast.className = `toast ${ok ? "ok" : "bad"} show`;
    toast.textContent = msg;
    toast.classList.remove("hidden");

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.classList.add("hidden"), 200);
    }, 1600);
}

function setLoadingList(on) {
    if (on) {
        notesList.innerHTML = `
      <div class="empty">
        <div class="spin"></div>
        <div>Loading notes...</div>
      </div>
    `;
    }
}

function renderNotes(notes) {
    const q = (searchNotes.value || "").toLowerCase().trim();
    const filtered = notes.filter(n => n.toLowerCase().includes(q));

    notesCount.textContent = `${filtered.length} notes`;

    if (!filtered.length) {
        notesList.innerHTML = `
      <div class="empty">
        <div>Nothing here.</div>
      </div>
    `;
        return;
    }

    notesList.innerHTML = "";
    for (const n of filtered) {
        const div = document.createElement("div");
        div.className = "item";
        div.innerHTML = `
      <div class="name">${escapeHtml(n)}</div>
      <div class="badge">click</div>
    `;
        div.addEventListener("click", () => {
            readName.value = n;
            showToast("Loaded into Read panel ✅", true);
        });
        notesList.appendChild(div);
    }
}

function escapeHtml(s) {
    return String(s)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
}

async function apiList() {
    setLoadingList(true);
    try {
        const r = await fetch("/list");
        const j = await r.json();
        const notes = Array.isArray(j.notes) ? j.notes : [];
        renderNotes(notes);
        return notes;
    } catch (e) {
        notesList.innerHTML = `
      <div class="empty">
        <div>Failed to load list.</div>
      </div>
    `;
        showToast("List failed", false);
        return [];
    }
}

async function apiCreate() {
    const name = createName.value.trim();
    const body = createBody.value;

    if (!name || !body) {
        showToast("Name & body required", false);
        return;
    }

    btnCreate.disabled = true;
    btnCreate.textContent = "Creating...";

    try {
        const form = new URLSearchParams();
        form.set("name", name);
        form.set("body", body);

        const r = await fetch("/create", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: form.toString(),
        });

        const j = await r.json().catch(() => ({}));

        if (r.status === 200) {
            showToast("Created ✅", true);
            createName.value = "";
            createBody.value = "";
            await apiList();
        } else {
            showToast("Failed", false);
        }
    } catch {
        showToast("Failed", false);
    } finally {
        btnCreate.disabled = false;
        btnCreate.textContent = "Create";
    }
}

async function apiRead() {
    const name = readName.value.trim();
    if (!name) {
        showToast("Name required", false);
        return;
    }

    btnRead.disabled = true;
    btnRead.textContent = "Reading...";
    readOutput.textContent = "(loading...)";

    try {
        const r = await fetch(`/read?name=${encodeURIComponent(name)}`);
        const t = await r.text();

        if (r.ok) {
            readOutput.textContent = t || "(empty)";
            showToast("Read ✅", true);
        } else {
            readOutput.textContent = t || "(not found)";
            showToast("Not found", false);
        }
    } catch {
        readOutput.textContent = "(error)";
        showToast("Read failed", false);
    } finally {
        btnRead.disabled = false;
        btnRead.textContent = "Read";
    }
}

btnCreate.addEventListener("click", apiCreate);
btnRead.addEventListener("click", apiRead);
btnRefresh.addEventListener("click", apiList);

btnClear.addEventListener("click", () => {
    readOutput.textContent = "(empty)";
    readName.value = "";
    showToast("Cleared", true);
});

btnCopy.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(readOutput.textContent || "");
        showToast("Copied ✅", true);
    } catch {
        showToast("Copy failed", false);
    }
});

btnCreateFill.addEventListener("click", () => {
    createName.value = "todo";
    createBody.value = "1) learn exploit\n2) read flag\n3) ???\n4) profit";
    showToast("Filled ✅", true);
});

searchNotes.addEventListener("input", async () => {
    // re-render without re-fetch
    const r = await fetch("/list");
    const j = await r.json().catch(() => ({}));
    renderNotes(Array.isArray(j.notes) ? j.notes : []);
});

// Initial load
apiList();
