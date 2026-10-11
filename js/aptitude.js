(() => {
  const root = document.getElementById("aptTest"), form = document.getElementById("testForm");
  const qs = [...document.querySelectorAll(".question")];
  const counter = document.getElementById("counter"), bar = document.getElementById("progress");
  const prev = document.getElementById("prev"), next = document.getElementById("next"), submit = document.getElementById("submit");
  const dotsBox = document.getElementById("dots"), answeredEl = document.getElementById("answeredCount"), timerEl = document.getElementById("timer");
  let current = 0, left = parseInt(root.dataset.seconds, 10), finished = false;

  const dots = qs.map((_, i) => { const d = document.createElement("button"); d.type = "button"; d.textContent = i + 1; d.addEventListener("click", () => show(i)); dotsBox.appendChild(d); return d; });
  const answered = i => !!qs[i].querySelector("input:checked");
  function refresh() {
    let n = 0;
    dots.forEach((d, i) => { d.classList.toggle("current", i === current); d.classList.toggle("done", answered(i)); if (answered(i)) n++; });
    answeredEl.textContent = n + " answered";
  }
  function show(i) {
    current = Math.max(0, Math.min(i, qs.length - 1));
    qs.forEach((q, n) => q.classList.toggle("active", n === current));
    counter.textContent = "Question " + (current + 1) + " of " + qs.length;
    bar.style.width = ((current + 1) / qs.length * 100) + "%";
    prev.disabled = current === 0;
    next.style.display = current === qs.length - 1 ? "none" : "inline-flex";
    submit.style.display = current === qs.length - 1 ? "inline-flex" : "none";
    refresh();
  }
  next.addEventListener("click", () => show(current + 1));
  prev.addEventListener("click", () => show(current - 1));
  form.addEventListener("change", refresh);

  function fmt(s) { return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); }
  const tick = setInterval(() => {
    left--; timerEl.textContent = fmt(Math.max(left, 0));
    timerEl.parentElement.classList.toggle("low", left <= 60);
    if (left <= 0) { clearInterval(tick); finished = true; form.submit(); }   // time is up: submit what has been answered
  }, 1000);

  form.addEventListener("submit", e => {
    if (finished) return;
    const missing = qs.filter((_, i) => !answered(i)).length;
    if (missing && !confirm(missing + " question(s) are unanswered and will count as wrong. Submit anyway?")) { e.preventDefault(); return; }
    finished = true; clearInterval(tick);
  });
  window.addEventListener("beforeunload", e => { if (!finished) { e.preventDefault(); e.returnValue = ""; } });
  show(0);
})();
