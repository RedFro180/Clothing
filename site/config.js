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
  // Shipping shown on products and in the preorder list. PLACEHOLDERS: set your real numbers.
  SHIPPING_FLAT: 9,                    // dollars per order
  FREE_SHIP_QTY: 2,                    // free shipping when the order has this many hoodies (0 = never)
  // Private analytics (only you see it). Make a free PostHog account, copy the "Project API key", paste it here.
  POSTHOG_KEY: "",
  POSTHOG_HOST: "https://us.i.posthog.com",
  // Order limits (protect against huge or fake orders). Large orders are still accepted but marked for you to check.
  MAX_QTY_PER_ITEM: 3,                 // most of one design + size a shopper can add
  MAX_ITEMS_PER_ORDER: 8,              // most hoodies in one preorder request
  LARGE_ORDER_ITEMS: 4,                // at this many hoodies the request is flagged "large order: verify before payment"
  // Sizes that are out of stock, by design number (the number at the start of each image name).
  // Example: SOLD_OUT: { 11: ["S", "3XL"], 27: ["M"] }. Shoppers can ask to be told when it's back.
  SOLD_OUT: {},
  // Show the "Text me" option for restock alerts. Only turn on once you have an SMS tool that
  // records consent and can send the texts (e.g. a Shopify back-in-stock or SMS app).
  SMS_ENABLED: false,
  // Social links for the footer. Leave "" to hide.
  INSTAGRAM: "",
  TIKTOK: "",
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
