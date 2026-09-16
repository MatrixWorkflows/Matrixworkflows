<p align="center">
  <img src="assets/banner.svg" alt="matrixworkflows banner — matrix rain, floating isometric cubes, terminal cursor" width="880" />
</p>

<!-- ⬡ 3D upgrade — page system inspired by Mayank Bhaskar's hearth README (github.com/qtjg/hearth) -->

<div align="center">

**matrixworkflows** · automation built and run solo — India · ![products](https://img.shields.io/badge/products-4-00ff9c?style=flat&labelColor=0d1117) ![follow](https://img.shields.io/github/followers/MatrixWorkflows?style=flat&labelColor=0d1117&color=00d4ff&label=follow)

<a href="https://github.com/MatrixWorkflows"><img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=20&duration=3200&pause=900&color=00FF9C&center=true&vCenter=true&width=860&height=72&lines=bots+that+sell+%C2%B7+systems+that+run+themselves;SellStack+%C2%B7+SubWala+%C2%B7+Cleo+%C2%B7+WhatsApp+AI;Telegram+%C2%B7+WhatsApp+%C2%B7+n8n+%C2%B7+MongoDB+%C2%B7+Docker" alt="matrixworkflows in one breath"/></a>

**I build automation that sells: Telegram bots, WhatsApp agents, and the stack underneath them.**

*SellStack — multi-tenant SaaS · SubWala — the n8n bot fleet · Cleo — a personal AI assistant · WhatsApp AI — agents that answer business inboxes*

<img src="assets/divider.svg" width="100%" alt=""/>

</div>

🟢 **Live right now:** Netflix · Crunchyroll · Amazon Prime · Spotify subscriptions — sold over Telegram, paid by plain UPI.

<details open>
<summary><strong>📑 Jump around</strong> — the whole README, indexed</summary>

[⚙️ The System](#-the-system-in-3d) · [🛰️ The Fleet](#-the-fleet) · [📈 Contributions](#-contributions) · [🧱 The Stack](#-the-stack) · [🤝 Made by matrixworkflows](#-made-by-matrixworkflows) · [🧊 3D Visuals](#-3d-visuals)

</details>

---

## ⚙️ The System, in 3D

Every diagram in this README is hand-built, zero-dependency animated SVG — pure CSS and SMIL, no JavaScript, no third-party widgets. The generators live in [`tools/`](tools/) and write into `assets/`. They float and pulse right on GitHub, and they're lossless at any zoom.

<img src="assets/system.svg" width="100%" alt="Isometric 3D diagram: Telegram and WhatsApp channel slabs feeding four product cubes — SellStack, SubWala, Cleo, WhatsApp AI — standing on a platform slab of n8n, MongoDB and Docker"/>

One message path, start to finish: a customer opens a bot, the webhook lands on the right tenant, an order gets its own unique UPI amount, the payment is confirmed, credentials go out, and cron quietly handles every expiry and renewal after that. The same spine carries all four products. Only the blocks on top change.

```mermaid
flowchart LR
    U["👤 customer"] --> H["webhook<br/>bots.matrixworkflows.in"]
    H --> R["tenant router<br/>/wh/id/role"]
    R --> B["bot logic<br/>Telegraf + Express"]
    B --> O["order + unique UPI amount"]
    O --> C["payment confirmed"]
    C --> K["credentials + license key delivered"]
    B --> D[("MongoDB Atlas")]
    D --> N["cron"]
    N --> E["expiry · renewal reminders · cleanup"]
```

## 🛰️ The Fleet

<img src="assets/projects.svg" width="100%" alt="SellStack, SubWala, Cleo and WhatsApp AI as four floating isometric cubes"/>

| Product | What it does | State |
|:---|:---|:---|
| 🛒 **SellStack** | multi-tenant SaaS — resellers run branded Telegram shops and an admin app off one codebase | 🔨 in build, serving its first tenants |
| 📦 **SubWala** | the n8n fleet that started it all — subscription reselling with live paying customers | 🟢 live |
| 🧠 **Cleo** | personal AI assistant on Telegram — calendar, mail, memory, tasks | 🟢 daily driver |
| 💬 **WhatsApp AI** | sales agents answering customers inside WhatsApp, per-tenant knowledge base, GPT-4.1 mini | 🟢 live since July |

## 📈 Contributions

<img src="assets/skyline.svg" width="100%" alt="3D isometric contribution skyline — one cube per real day"/>

Every cube is one real day pulled from GitHub's GraphQL contribution calendar and regenerated daily by a GitHub Action. The account is new; the work started a year ago in private repos and on production servers.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MatrixWorkflows/Matrixworkflows/gh-pages/github-contribution-grid-snake-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/MatrixWorkflows/Matrixworkflows/gh-pages/github-contribution-grid-snake.svg"/>
  <img src="https://raw.githubusercontent.com/MatrixWorkflows/Matrixworkflows/gh-pages/github-contribution-grid-snake.svg" width="100%" alt="contribution snake — light and dark variants swap with your GitHub theme"/>
</picture>

## 🧱 The Stack

<img src="assets/stack.svg" width="100%" alt="An exploded isometric stack — runtime, core, ship and ai layers floating on a rising axis"/>

TypeScript · Node.js · Express · MongoDB Atlas · React Native + Expo · Python · Docker · Linux · n8n · Telegraf · Baileys · Zod · GPT-4.1 mini

---

## 🤝 Made by matrixworkflows

<div align="center">

### designed · engineered · deployed · operated by one person

The bots, the SaaS, the infrastructure, and every animated SVG on this page — designed, written, deployed and run by one person from India. Four products on one VPS.

<a href="mailto:matrixworkflows@gmail.com"><img src="https://img.shields.io/badge/matrixworkflows%40gmail.com-00ff9c?style=for-the-badge&labelColor=1b1f2a&logo=gmail&logoColor=04100b" alt="email"/></a>
<a href="https://matrixworkflows.in"><img src="https://img.shields.io/badge/matrixworkflows.in-00d4ff?style=for-the-badge&labelColor=1b1f2a" alt="website"/></a>
<a href="https://github.com/MatrixWorkflows"><img src="https://img.shields.io/badge/github-%40MatrixWorkflows-ffb454?style=for-the-badge&labelColor=1b1f2a&logo=github" alt="github"/></a>

<br/>

<img src="assets/divider.svg" width="100%" alt=""/>

## 🧊 3D Visuals

Every graphic here is generated, nothing hand-drawn — stdlib-only Python, no dependencies, no external services. Regenerate any of them:

```bash
python tools/generate_banner.py    # the matrix rain banner
python tools/generate_projects.py  # the fleet, as iso cubes
python tools/generate_system.py    # the system diagram
python tools/generate_stack.py     # the exploded stack
python tools/generate_divider.py   # the data-bus divider
python tools/generate_skyline.py --user MatrixWorkflows  # needs GITHUB_TOKEN
```

<img src="https://capsule-render.vercel.app/api?type=waving&height=110&color=0:0f8f63,50:00ff9c,100:00d4ff&section=footer" width="100%" alt=""/>

<sub>**matrixworkflows** — bots that sell · systems that run themselves.</sub>

</div>
