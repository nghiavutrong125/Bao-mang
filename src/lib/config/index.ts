import type { Link } from "../types";

export const SITE = {
  title: "50fiftymagazine",
  description: "Unfiltered Travel, Culture & Honest Perspectives.",
  author: "The Editorial Desk",
  url: "https://50fiftymagazine.com",
  github: "https://github.com",
  locale: "en-US",
  dir: "ltr",
  charset: "UTF-8",
  basePath: "/",
  postsPerPage: 6,
  googleSiteVerification: import.meta.env.PUBLIC_GOOGLE_SITE_VERIFICATION || "",
  googleAnalyticsId: import.meta.env.PUBLIC_GA_ID || "G-01LKYRCLK2",
};

export const NAVIGATION_LINKS: Link[] = [
  {
    href: "/categories/destinations",
    text: "Destinations",
  },
  {
    href: "/categories/reviews",
    text: "Honest Reviews",
  },
  {
    href: "/categories/travel-tips",
    text: "Tips & Scams",
  },
  {
    href: "/categories/culture",
    text: "Culture & Food",
  },
];

export const OTHER_LINKS: Link[] = [
  {
    href: "/about",
    text: "About us",
  },
  {
    href: "/authors",
    text: "Authors",
  },
  {
    href: "/contact",
    text: "Contact",
  },
  {
    href: "/privacy",
    text: "Privacy",
  },
  {
    href: "/terms",
    text: "Terms",
  },
  {
    href: "/cookie-policy",
    text: "Cookie Policy",
  },
  {
    href: "/rss.xml",
    text: "RSS",
  },
  {
    href: "/sitemap-index.xml",
    text: "Sitemap",
  },
];

export const SOCIAL_LINKS: Link[] = [
  {
    href: "https://twitter.com",
    text: "Twitter",
    icon: "newTwitter",
  },
  {
    href: "https://www.facebook.com",
    text: "Facebook",
    icon: "facebook",
  },
];
