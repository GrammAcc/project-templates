const populatePage = async () => {
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
