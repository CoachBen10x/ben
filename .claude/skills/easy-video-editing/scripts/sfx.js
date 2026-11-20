#!/usr/bin/env node
// Make a sound effect .wav with jsfx (github.com/loov/jsfx, MIT).
// Usage: node sfx.js PRESET out.wav [--seed N] [--vol 0.6]
//        node sfx.js '{"Volume":{"Sustain":0.1,"Decay":0.15,"Punch":0.55}}' out.wav
// Presets: Coin, Laser, Explosion, Powerup, Hit, Jump, Select, Lucky
const fs = require("fs"), path = require("path");
global.window = {};                              // jsfx was written for browsers; it only needs this to exist
const jsfx = require(path.join(__dirname, "jsfx.js"));
jsfx.SetSampleRate(44100);
const a = process.argv.slice(2);
if (a.length < 2) { console.log("presets:", Object.keys(jsfx.Preset).filter(k => k !== "Reset").join(", ")); process.exit(1); }
const opt = (k, d) => { const i = a.indexOf(k); return i > 0 ? +a[i + 1] : d; };
let seed = opt("--seed", 1);                       // same seed = same sound every time
Math.random = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
const params = a[0].trim().startsWith("{") ? JSON.parse(a[0]) : jsfx.Preset[a[0]]?.();
if (!params) { console.error("unknown preset", a[0]); process.exit(1); }
const vol = opt("--vol", 0.6), buf = jsfx.FloatBuffer(params);
for (let i = 0; i < buf.length; i++) buf[i] = Math.max(-1, Math.min(1, buf[i] * vol));
fs.writeFileSync(a[1], Buffer.from(jsfx.CreateWave(buf)));
console.log(`${a[0].slice(0, 30)} -> ${a[1]} (${(buf.length / 44100).toFixed(2)}s)`);
