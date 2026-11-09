# xgassman.com

A small gallery of browser games and tools I've made, live at **[xgassman.com](https://xgassman.com)**.

## Projects

### Sawyer's Skateboarding Superpets
`superpets.html`

Made for my daughter and her pets. Inspired by the Rotunda of Gateways in *Doctor Strange*: think Flappy Bird meets the endless hallways of Tom & Jerry and old Hanna-Barbera cartoons, then add a double jump. Version 2 will bring power-ups, difficulty settings, a difficulty curve that ramps up as you go, and high scores (pending Twin Galaxies approval).

### Dice
`dice.html`

For when you don't have the right dice on hand for a board game, or anything else.

### Spectrum Studio
`spectrum-studio.html`

Turn on your microphone and you've got a visualizer that moves with sound and music, with presets and plenty of ways to customize the look. Inspired by the Winamp visualization plugins of the late '90s and early 2000s. Winamp, it really whips the llama's ass!

### Idea Board
`idea-board.html`

My own take on Stickies, because I live in a world of Chrome tabs. Notes, photos and links save in your browser.

### Da Chicago Pope Hot Dog Dropper Game
`hot-dog-dropper.html`

A Chicago street-food drop game. Inspired by the 1995 freeware Mac game [Slick Willie 2.0](https://www.macintoshrepository.org/6705-slick-willie-2-0) by Jim Byer.

### Downhill
`downhill.html`

A pixel-art downhill skiing game inspired by [SkiFree](https://en.wikipedia.org/wiki/SkiFree), the 1991 Windows classic made by Chris Pirih. Pick Free Ski, Slalom or Freestyle, jump, pull tricks in the air, rack up style points, and watch out after 1500 m...

### Cake Land
`cake-land/`

A top-down, 16-bit style adventure starring Pancake, an anthropomorphic pancake with a bubble wand. Explore the village, fish the Syrup River, trade for hats that change your shots, befriend the Leafy pets, and face Mr. Thunderman.

### Langton's Ant
`langtons-ant.html`

A simulation with two rules: on a dark square turn right, on a lit square turn left. Watch about 10,000 steps of chaos turn into a "highway", or try custom grids and up to four ants.

Everything is plain HTML, CSS and JavaScript: no build step, no dependencies.

## Folder layout

```
index.html      the gallery page
*.html          one file per project
cake-land/      Cake Land (game page plus its fonts and sprite art)
images/         artwork for Superpets
icons/          gallery tile icons (source copies; index.html has them built in)
favicons/       browser-tab and home-screen icons for each page
CNAME           custom domain for GitHub Pages (managed by GitHub)
```

## Hosting

Served by **GitHub Pages** from the `main` branch, root folder. The domain is registered at Squarespace, with DNS pointing to GitHub:

- `A @` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
- `CNAME www` → mgassman321.github.io

## Updating the site

```
cd ~/Documents/xgassman
git pull                     # always first: picks up changes made on github.com
git add -A
git commit -m "Describe the change"
git push
```

Changes appear on xgassman.com about a minute after pushing.

## Adding a project

1. Put the new `.html` file in this folder.
2. In `index.html`, copy one of the `<li>` tiles in the grid, then change the link, name and class.
3. Add a matching color line in the "Tile colors" CSS block.
4. Add a favicon by copying the two `<link rel="icon">` lines from another project page.

To preview locally, open `index.html` in a browser, or run `python3 -m http.server` here and visit http://localhost:8000.
