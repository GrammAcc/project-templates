from pathlib import Path


spa = """<!doctype html>
<html lang="en">
  <head>
    <title>Project Template SPA</title>
    <link rel="icon" href="data:,">
    <script crossorigin="anonymous" src="/main.js"></script>
  </head>
  <body>
    <main>
      <h1 id="heading">Project Template SPA</h1>
    </main>
  </body>
</html>
"""

static_root = """<!doctype html>
<html lang="en">
  <head>
    <title>Project Template Static Site</title>
    <link rel="icon" href="data:,">
    <script crossorigin="anonymous" src="/main.js"></script>
  </head>
  <body>
    <main>
      <h1 id="heading">Project Template Static Site</h1>
    </main>
  </body>
</html>
"""

static_page = """<!doctype html>
<html lang="en">
  <head>
    <title>Project Template Static Page</title>
    <link rel="icon" href="data:,">
    <script crossorigin="anonymous" src="/main.js"></script>
  </head>
  <body>
    <main>
      <h1 id="heading">Project Template Static Page</h1>
    </main>
  </body>
</html>
"""

static_nested_page = """<!doctype html>
<html lang="en">
  <head>
    <title>Project Template Static Nested Page</title>
    <link rel="icon" href="data:,">
    <script crossorigin="anonymous" src="/main.js"></script>
  </head>
  <body>
    <main>
      <h1 id="heading">Project Template Static Nested Page</h1>
    </main>
  </body>
</html>
"""

js = """const populatePage = async () => {
  const heading = document.querySelector("#heading")
  const res = await fetch("/api/v1/replace-me", {
    method: "GET",
  })
  const data = await res.json()
  let newHTML = "<p>This was populated by Javascript.</p>"
  for (const record of data) {
    newHTML += `<pre>Example resource: ${record.name}</pre>`
  }
  heading.insertAdjacentHTML("afterend", newHTML)
}

if (document.readyState !== 'loading') {
  populatePage()
} else {
  document.addEventListener('DOMContentLoaded', () => {
    populatePage()
  })
}
"""


print("Creating any missing directories...")

spa_site_dir = Path("src/packagename/frontend/spa/site")
if not spa_site_dir.exists():
    spa_site_dir.mkdir()

static_site_dir = Path("src/packagename/frontend/static/site")
if not static_site_dir.exists():
    static_site_dir.mkdir()

nested_static_page_dir = static_site_dir / "nested"

if not nested_static_page_dir.exists():
    nested_static_page_dir.mkdir()


print("Building spa site...")

with open(spa_site_dir / "main.js", "w") as js_file:
    js_file.write(js)
with open(spa_site_dir / "index.html", "w") as html_file:
    html_file.write(spa)


print("Building static html/js/css site...")

with open(static_site_dir / "main.js", "w") as js_file:
    js_file.write(js)
with open(static_site_dir / "index.html", "w") as html_file:
    html_file.write(static_root)
with open(static_site_dir / "page.html", "w") as html_file:
    html_file.write(static_page)
with open(nested_static_page_dir / "page.html", "w") as html_file:
    html_file.write(static_nested_page)

print("Done!")
