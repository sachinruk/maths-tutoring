const track = (name, params) => { if (typeof gtag === "function") gtag("event", name, params); };

const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

const form = document.querySelector(".contact-form");
if (form) form.addEventListener("submit", () => track("generate_lead", { method: "form" }));

document.querySelectorAll('a[href^="https://wa.me/"]').forEach((a) => a.addEventListener("click", () => track("generate_lead", { method: "whatsapp" })));
document.querySelectorAll('a[href^="sms:"]').forEach((a) => a.addEventListener("click", () => track("generate_lead", { method: "sms" })));
document.querySelectorAll('a[href^="mailto:"]').forEach((a) => a.addEventListener("click", () => track("generate_lead", { method: "email" })));
document.querySelectorAll('a[href$="#contact"]').forEach((a) => a.addEventListener("click", () => track("trial_cta_click", { cta_text: a.textContent.trim() })));

document.querySelectorAll(".video-facade").forEach((btn) => {
  btn.addEventListener("click", () => {
    track("video_play", { video_title: btn.getAttribute("aria-label").replace("Play: ", "") });
    const src = btn.dataset.list
      ? `https://www.youtube-nocookie.com/embed/videoseries?list=${btn.dataset.list}&autoplay=1`
      : `https://www.youtube-nocookie.com/embed/${btn.dataset.id}?autoplay=1&rel=0`;
    const iframe = document.createElement("iframe");
    Object.assign(iframe, { src, title: btn.getAttribute("aria-label"), allowFullscreen: true });
    iframe.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture";
    iframe.className = "video-frame";
    btn.replaceWith(iframe);
  });
});

const phone = document.getElementById("phone");
if (phone) {
  phone.addEventListener("input", (e) => {
    e.target.value = e.target.value.replace(/[^0-9+]/g, "").replace(/(?!^)\+/g, "");
  });
}
