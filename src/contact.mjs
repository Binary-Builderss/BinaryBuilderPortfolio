// Pure helpers for the contact form, kept free of Workers imports so Node can test them.

export const FROM = "form@binarybuilders.dev";
export const SERVICES = ["Custom software", "Backend and API integration", "Salesforce", "Maintenance", "Other"];

// Strip CR/LF so user input can never inject extra mail headers.
const oneLine = (s) => s.replace(/[\r\n]+/g, " ").trim();

export function parseForm(form) {
  if (form.get("website")) return { spam: true }; // honeypot, real users never see it
  const get = (k) => String(form.get(k) ?? "").trim();
  const f = {
    name: oneLine(get("name")),
    email: oneLine(get("email")),
    company: oneLine(get("company")),
    service: get("service"),
    message: get("message"),
  };
  const ok =
    f.name.length > 0 && f.name.length <= 100 &&
    f.email.length <= 200 && /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(f.email) &&
    f.company.length <= 120 &&
    SERVICES.includes(f.service) &&
    f.message.length >= 10 && f.message.length <= 5000;
  return ok ? { fields: f } : { invalid: true };
}

const b64 = (s) => {
  let bin = "";
  for (const byte of new TextEncoder().encode(s)) bin += String.fromCharCode(byte);
  return btoa(bin);
};

export function buildMime(f, to, id = crypto.randomUUID(), date = new Date()) {
  const body = [
    `Name: ${f.name}`,
    `Email: ${f.email}`,
    `Company: ${f.company || "-"}`,
    `Service: ${f.service}`,
    "",
    f.message,
  ].join("\r\n");
  return [
    `From: BinaryBuilders website <${FROM}>`,
    `To: <${to}>`,
    `Reply-To: <${f.email}>`,
    `Subject: =?UTF-8?B?${b64(`New project request: ${f.service} from ${f.name}`)}?=`,
    `Message-ID: <${id}@binarybuilders.dev>`,
    `Date: ${date.toUTCString()}`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=utf-8",
    "Content-Transfer-Encoding: base64",
    "",
    b64(body).replace(/.{76}/g, "$&\r\n"),
  ].join("\r\n");
}
