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
  // Business details for the policies page and footer. Card networks, Shopify, TikTok Shop and ad platforms expect these.
  BUSINESS_NAME: "",                   // legal name, e.g. "Your Name LLC"
  BUSINESS_ADDRESS: "",                // mailing address or registered PO box (also required in marketing emails: CAN-SPAM)
  // Ship time stated to buyers (FTC Mail Order Rule: if none is stated you must be able to ship within 30 days).
  SHIP_WINDOW: "",                     // e.g. "Ships 4–6 weeks after payment"
  ORIGIN: "",                          // country of origin shown on every product, e.g. "Made in USA" or "Imported"
  POLICY_UPDATED: "",                  // date the policies were last updated, e.g. "2026-12-01"
  CURRENCY: "USD",
  // Shipping shown on products and in the preorder list. PLACEHOLDERS: set your real numbers.
  SHIPPING_FLAT: 9,                    // dollars per order
  FREE_SHIP_OVER: 200,                 // free shipping when the order subtotal is this many dollars or more (0 = off)
  FREE_SHIP_QTY: 0,                    // or: free shipping at this many items (0 = off). Item counts include cheap socks, so dollars is safer.
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
  // Size guides for the other items (same idea: blank = "Measurements coming soon"). Hats are one size.
  SIZE_CHARTS: {
    tee: [
      { size: "S", chest: "", length: "", sleeve: "" }, { size: "M", chest: "", length: "", sleeve: "" },
      { size: "L", chest: "", length: "", sleeve: "" }, { size: "XL", chest: "", length: "", sleeve: "" },
      { size: "2XL", chest: "", length: "", sleeve: "" }, { size: "3XL", chest: "", length: "", sleeve: "" },
      { size: "4XL", chest: "", length: "", sleeve: "" },
    ],
    underwear: [
      { size: "S", waist: "", inseam: "" }, { size: "M", waist: "", inseam: "" }, { size: "L", waist: "", inseam: "" },
      { size: "XL", waist: "", inseam: "" }, { size: "2XL", waist: "", inseam: "" },
    ],
    socks: [
      { size: "S/M", us_men: "", us_women: "" }, { size: "L/XL", us_men: "", us_women: "" },
    ],
    sweatpants: [
      { size: "S", waist: "", hip: "", inseam: "" }, { size: "M", waist: "", hip: "", inseam: "" },
      { size: "L", waist: "", hip: "", inseam: "" }, { size: "XL", waist: "", hip: "", inseam: "" },
      { size: "2XL", waist: "", hip: "", inseam: "" }, { size: "3XL", waist: "", hip: "", inseam: "" },
      { size: "4XL", waist: "", hip: "", inseam: "" },
    ],
  },
  SIZE_UNITS: "in",
  SIZE_CHART: [
    { size: "S",   chest: "", length: "", sleeve: "" },
    { size: "M",   chest: "", length: "", sleeve: "" },
    { size: "L",   chest: "", length: "", sleeve: "" },
    { size: "XL",  chest: "", length: "", sleeve: "" },
    { size: "2XL", chest: "", length: "", sleeve: "" },
    { size: "3XL", chest: "", length: "", sleeve: "" },
    { size: "4XL", chest: "", length: "", sleeve: "" },
  ],
  // How each item fits and fabric weight, shown on every product and in the size guide. Blank = hidden.
  // All sales are final, so fill these in: e.g. FIT hoodie "Relaxed, boxy fit. True to size; size down for a closer fit." WEIGHT hoodie "400 GSM".
  FIT: { hoodie: "", tee: "", sweatpants: "", underwear: "", socks: "", hats: "" },
  WEIGHT: { hoodie: "", tee: "", sweatpants: "" },
  // "Get the set" (hoodie + sweatpants in the same design). Dollars off when both are in one order; 0 = no discount.
  SET_DISCOUNT: 0,
  // Small "get first access to new drops" card: shows once after 30 seconds or the 2nd product opened, then not again for 30 days.
  DROP_PROMPT: true,
  // About section. Leave text "" to hide it. Template (replace with your own words):
  //   title: "Who makes this"
  //   text: "I'm [name], a lifter from Ohio. I make every piece in small batches from hemp, cotton and wool, with no plastic,
  //          because what touches your skin all day should be real. The jokes are dark because life can be. They're for
  //          getting through it, not giving up. If it's more than a joke tonight, call or text 988."
  //   photo: "photos/about.jpg" (optional; put the file in site/photos)
  ABOUT: { title: "", text: "", photo: "" },
  // The spinning ring at the top shows the Featured hoodies (FEATURED in tools/build_site.py).
  HERO_SPEED: 24,                      // seconds for one full turn of the ring; bigger = slower
};
