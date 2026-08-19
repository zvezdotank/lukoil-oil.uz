(function () {
"use strict";
var MAIL = "i.kim@lukoil-oil.uz";
var burger = document.querySelector(".burger");
var nav = document.getElementById("nav");
if (burger && nav) {
burger.addEventListener("click", function () {
var open = nav.classList.toggle("open");
burger.setAttribute("aria-expanded", open ? "true" : "false");
});
}
var modal = document.getElementById("callback");
var lastFocus = null;
function openModal() {
if (!modal) return;
lastFocus = document.activeElement;
modal.hidden = false;
var f = modal.querySelector("input");
if (f) f.focus();
}
function closeModal() {
if (!modal) return;
modal.hidden = true;
if (lastFocus) lastFocus.focus();
}
document.addEventListener("click", function (e) {
var t = e.target.closest ? e.target.closest("[data-callback]") : null;
if (t) { e.preventDefault(); openModal(); return; }
if (e.target.closest && e.target.closest("[data-close]")) { e.preventDefault(); closeModal(); }
if (modal && !modal.hidden && e.target === modal) closeModal();
});
document.addEventListener("keydown", function (e) {
if (e.key === "Escape" && modal && !modal.hidden) closeModal();
});
var finder = document.getElementById("finder");
if (finder && window.CATALOG) {
var tbody = finder.querySelector("tbody");
function render(key) {
var rows = window.CATALOG[key] || [];
tbody.innerHTML = rows.map(function (r) {
return "<tr><td>" + r[0] + "</td><td><strong>" + r[1] + "</strong></td><td>" +
r[2] + "</td><td>" + r[3] + "</td><td><span class=\"tag tag-accent\">" + r[4] + "</span></td></tr>";
}).join("");
}
finder.addEventListener("change", function (e) {
if (e.target.name === "seg") render(e.target.value);
});
var checked = finder.querySelector("input[name=seg]:checked");
if (checked) render(checked.value);
}
function collect(form) {
var d = {};
Array.prototype.forEach.call(form.elements, function (el) {
if (!el.name || el.type === "submit") return;
if (el.type === "radio") { if (el.checked) d[el.name] = el.value; }
else d[el.name] = el.value.trim();
});
return d;
}
document.addEventListener("submit", function (e) {
var form = e.target;
if (!form.matches("[data-mailform]")) return;
e.preventDefault();
var d = collect(form);
var kind = d.kind || "Заявка";
var lines = [];
if (d.name) lines.push("Имя: " + d.name);
if (d.company) lines.push("Организация: " + d.company);
if (d.phone) lines.push("Телефон: " + d.phone);
if (d.note) lines.push("", "Задача:", d.note);
lines.push("", "Страница: " + location.href);
var subject = kind + " с сайта lukoil-oil.uz";
var href = "mailto:" + MAIL +
"?subject=" + encodeURIComponent(subject) +
"&body=" + encodeURIComponent(lines.join("\n"));
var box = form.parentNode.querySelector("[data-sent]");
if (box) {
form.hidden = true;
box.hidden = false;
var link = box.querySelector("[data-sent-link]");
if (link) link.href = href;
var who = box.querySelector("[data-sent-name]");
if (who) who.textContent = d.name ? ", " + d.name : "";
}
window.location.href = href;
});
document.addEventListener("click", function (e) {
var b = e.target.closest ? e.target.closest("[data-again]") : null;
if (!b) return;
e.preventDefault();
var box = b.closest("[data-sent]");
var form = box.parentNode.querySelector("[data-mailform]");
box.hidden = true;
form.hidden = false;
form.reset();
var f = form.querySelector("input");
if (f) f.focus();
});
})();