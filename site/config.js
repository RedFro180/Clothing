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
  // Hoodies that glide across the top of the page, in order. Use the design numbers
  // (the number at the start of each image name, e.g. 11 = img/11-skeleton-wearing-meat.svg).
  HERO_ROTATION: [11, 10, 27, 44, 29, 60, 13, 48],
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
  HERO_SPEED: 60,                      // seconds for one full loop of the top strip; bigger = slower
};
