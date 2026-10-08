// Run: node src/contact.test.mjs
import assert from "node:assert/strict";
import { parseForm, buildMime } from "./contact.mjs";

const form = (o) => new Map(Object.entries(o));
const valid = {
  name: "Ada Rossi",
  email: "ada@example.com",
  company: "",
  service: "Salesforce",
  message: "We need an Apex trigger fixed.",
};

assert.deepEqual(parseForm(form({ ...valid, website: "x" })), { spam: true });
assert.ok(parseForm(form(valid)).fields);
assert.ok(parseForm(form({ ...valid, email: "not-an-email" })).invalid);
assert.ok(parseForm(form({ ...valid, email: "a@b.co>\r\nBcc: x@y.z" })).invalid);
assert.ok(parseForm(form({ ...valid, service: "Hacking" })).invalid);
assert.ok(parseForm(form({ ...valid, message: "short" })).invalid);

// Header injection through the name must not create a new header line.
const { fields } = parseForm(form({ ...valid, name: "Eve\r\nBcc: victim@example.com" }));
const mime = buildMime(fields, "inbox@example.com", "id", new Date(0));
const headers = mime.split("\r\n\r\n")[0];
assert.ok(!/^Bcc:/m.test(headers));
assert.match(headers, /^Reply-To: <ada@example\.com>$/m);
assert.equal(atob(mime.split("\r\n\r\n")[1].replace(/\r\n/g, "")).includes("Apex trigger"), true);

console.log("contact form checks passed");
