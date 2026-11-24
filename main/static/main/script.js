(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // ---- Image slot labels: index.html?slots=1 shows them, ?slots=0 hides ----
  try {
    if (new URLSearchParams(location.search).get("slots") === "1") document.documentElement.classList.add("show-slots");
    if (new URLSearchParams(location.search).get("slots") === "1") document.body.classList.add("show-slots");
  } catch (e) {}

  document.getElementById("yr").textContent = new Date().getFullYear();

  // ---- Header shadow + mobile menu ----
  var header = $("#header"), nav = $("#nav"), burger = $("#burger");
  function onScroll() { header.classList.toggle("scrolled", window.scrollY > 8); }
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.classList.toggle("x", open);
    burger.setAttribute("aria-expanded", open);
  });
  $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { nav.classList.remove("open"); burger.classList.remove("x"); burger.setAttribute("aria-expanded", "false"); }); });

  // ---- Reveal on scroll ----
  var els = $$(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    els.forEach(function (el, i) { el.style.transitionDelay = ((i % 4) * 60) + "ms"; io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add("in"); }); }

  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }

  // ---- Services ----
  // Services come from the database (editable in the admin)
  var SERVICES = JSON.parse(document.getElementById("services-data").textContent);
  var tabs = $("#svcTabs"), panel = $("#svcPanel"), current = 0;
  var sel = $("#serviceSelect");
  SERVICES.forEach(function (s, i) {
    var b = document.createElement("button");
    b.className = "svc-tab"; b.setAttribute("role", "tab"); b.id = "svc-tab-" + i;
    b.innerHTML = "<span>" + String(i + 1).padStart(2, "0") + "</span>" + esc(s.t);
    b.addEventListener("click", function () { showService(i); });
    tabs.appendChild(b);
    var o = document.createElement("option"); o.value = s.t; o.textContent = s.t; sel.appendChild(o);
  });
  function paint(i) {
    var s = SERVICES[i];
    $("#svcImg").src = s.img; $("#svcImg").alt = s.t;
    $("#svcNo").textContent = String(i + 1).padStart(2, "0");
    $("#svcTitle").textContent = s.t; $("#svcDesc").textContent = s.d;
    $("#svcList").innerHTML = s.f.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("");
    $$(".svc-tab").forEach(function (t, k) { t.setAttribute("aria-selected", k === i ? "true" : "false"); });
  }
  function showService(i) {
    if (i === current) return;
    current = i; panel.classList.add("swap");
    setTimeout(function () { paint(i); panel.classList.remove("swap"); }, 260);
  }
  if (SERVICES.length) paint(0);
  // keyboard: arrows move between tabs
  tabs.addEventListener("keydown", function (e) {
    if (e.key !== "ArrowDown" && e.key !== "ArrowUp" && e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    e.preventDefault();
    var d = (e.key === "ArrowDown" || e.key === "ArrowRight") ? 1 : -1;
    var n = (current + d + SERVICES.length) % SERVICES.length;
    showService(n); setTimeout(function () { $("#svc-tab-" + n).focus(); }, 280);
  });
  $("#svcCta").addEventListener("click", function () { sel.value = SERVICES[current].t; });

  // ---- Gallery + lightbox ----
  // Projects come from the database (editable in the admin)
  var WORK = JSON.parse(document.getElementById("projects-data").textContent);
  var gal = $("#gallery"), shown = [], idx = 0;
  function renderGallery(f) {
    shown = WORK.filter(function (w) { return f === "all" || w.s === f; });
    gal.innerHTML = "";
    shown.forEach(function (w, i) {
      var b = document.createElement("button");
      b.className = "g-item slot"; b.setAttribute("data-slot", "Project photo"); b.setAttribute("data-size", "1200 × 900 px · JPG (4:3)");
      b.setAttribute("aria-label", "Open " + w.t);
      b.innerHTML = '<img src="' + w.img + '" alt="' + esc(w.t) + '" loading="lazy" /><span class="g-cap"><strong>' + esc(w.t) + "</strong><small>" + (w.s === "completed" ? "Completed" : "Ongoing") + "</small></span>";
      b.addEventListener("click", function () { openLb(i); });
      gal.appendChild(b);
    });
  }
  $$(".chip").forEach(function (c) {
    c.addEventListener("click", function () {
      $$(".chip").forEach(function (x) { x.classList.remove("on"); x.setAttribute("aria-selected", "false"); });
      c.classList.add("on"); c.setAttribute("aria-selected", "true");
      renderGallery(c.getAttribute("data-filter"));
    });
  });
  renderGallery("all");

  var lb = $("#lb"), lbImg = $("#lbImg"), lbCap = $("#lbCap");
  function showLb() { lbImg.src = shown[idx].img; lbImg.alt = shown[idx].t; lbCap.textContent = shown[idx].t + "  ·  " + (idx + 1) + " / " + shown.length; }
  function openLb(i) { idx = i; showLb(); lb.hidden = false; document.body.style.overflow = "hidden"; $(".lb-x").focus(); }
  function closeLb() { lb.hidden = true; document.body.style.overflow = ""; }
  function step(d) { idx = (idx + d + shown.length) % shown.length; showLb(); }
  $(".lb-x").addEventListener("click", closeLb);
  $(".lb-p").addEventListener("click", function () { step(-1); });
  $(".lb-n").addEventListener("click", function () { step(1); });
  lb.addEventListener("click", function (e) { if (e.target === lb) closeLb(); });
  document.addEventListener("keydown", function (e) {
    if (lb.hidden) return;
    if (e.key === "Escape") closeLb(); if (e.key === "ArrowRight") step(1); if (e.key === "ArrowLeft") step(-1);
  });

  // ---- FAQ accordion ----
  $$(".acc-q").forEach(function (q) {
    q.addEventListener("click", function () {
      var item = q.parentNode, open = item.classList.contains("open");
      $$(".acc-item").forEach(function (i) { i.classList.remove("open"); $(".acc-q", i).setAttribute("aria-expanded", "false"); });
      if (!open) { item.classList.add("open"); q.setAttribute("aria-expanded", "true"); }
    });
  });

  // ---- Enquiry form: opens WhatsApp (or email) with the message ready ----
  var WA = (window.SITE && window.SITE.wa) || "", MAIL = (window.SITE && window.SITE.mail) || "";
  var form = $("#enquiryForm"), msg = $("#formMsg");
  function compose() {
    var d = new FormData(form);
    return "Hello Expertz Acoustics & Interiors,\n\nName: " + (d.get("name") || "").trim() + "\nPhone: " + (d.get("phone") || "").trim() +
      "\nService: " + (d.get("service") || "Not specified") + "\n\n" + (d.get("message") || "").trim();
  }
  $("#mailAlt").addEventListener("click", function (e) {
    e.preventDefault();
    location.href = "mailto:" + MAIL + "?subject=" + encodeURIComponent("Enquiry from website") + "&body=" + encodeURIComponent(compose());
  });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var d = new FormData(form);
    var digits = String(d.get("phone") || "").replace(/\D/g, "");
    msg.className = "form-msg";
    if (!String(d.get("name") || "").trim() || !String(d.get("message") || "").trim()) { msg.textContent = "Please enter your name and a short message."; msg.classList.add("err"); return; }
    if (digits.length < 8) { msg.textContent = "Please enter a valid phone number."; msg.classList.add("err"); return; }
    window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent(compose()), "_blank", "noopener");
    msg.textContent = "Thank you! WhatsApp has opened with your message. Just press send."; msg.classList.add("ok");
    form.reset();
  });
})();
