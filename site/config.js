// Site settings. Change these, no code knowledge needed.
window.SITE_CONFIG = {
  BRAND: "Brand Name",                 // placeholder until you pick a name
  TAGLINE: "Dark humor. Natural fiber. No plastic.",
  // Label for the top row. Keep "Featured" until you have real sales; calling unsold
  // items "best sellers" is a false claim (FTC Act Section 5).
  FEATURED_LABEL: "Featured",
  // Where preorder / notify-me requests go.
  // FORM_ENDPOINT: a form service URL (e.g. a Formspree form URL). Leave "" to use email instead.
  FORM_ENDPOINT: "",
  CONTACT_EMAIL: "hello@example.com",  // replace with your shop email
  CURRENCY: "USD",
  // Size guide shown on every product. Fill in the numbers (garment measured flat). Blank = "Measurements coming soon".
  SIZE_UNITS: "in",
  SIZE_CHART: [
    { size: "S",   chest: "", length: "", sleeve: "" },
    { size: "M",   chest: "", length: "", sleeve: "" },
    { size: "L",   chest: "", length: "", sleeve: "" },
    { size: "XL",  chest: "", length: "", sleeve: "" },
    { size: "2XL", chest: "", length: "", sleeve: "" },
    { size: "3XL", chest: "", length: "", sleeve: "" },
  ],
  // The spinning ring at the top shows the Featured hoodies (FEATURED in tools/build_site.py).
  HERO_SPEED: 24,                      // seconds for one full turn of the ring; bigger = slower
};
