// Language switch shared by all pages: ?lang=ru | saved choice | browser language | uz
(function () {
  function safeGet() { try { return localStorage.getItem("qaytar-lang"); } catch (e) { return null; } }
  function safeSet(v) { try { localStorage.setItem("qaytar-lang", v); } catch (e) {} }

  var param = new URLSearchParams(location.search).get("lang");
  var nav = (navigator.language || "").toLowerCase().indexOf("ru") === 0 ? "ru" : "uz";
  var lang = (param === "ru" || param === "uz") ? param : (safeGet() || nav);

  window.setLang = function (l) {
    lang = l;
    document.documentElement.lang = l;
    safeSet(l);
    document.querySelectorAll("[data-set-lang]").forEach(function (b) {
      b.classList.toggle("active", b.getAttribute("data-set-lang") === l);
    });
    if (typeof window.applyI18n === "function") window.applyI18n(l);
  };
  window.getLang = function () { return lang; };

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-set-lang]").forEach(function (b) {
      b.addEventListener("click", function () { window.setLang(b.getAttribute("data-set-lang")); });
    });
    window.setLang(lang);
  });
})();
