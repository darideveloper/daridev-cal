document.addEventListener("DOMContentLoaded", () => {
  const noMarkdownIds = ["google_maps_src", "description", "google_calendar_credentials"]
  let textAreasSelector = 'div > textarea'
  const notSelector = noMarkdownIds.map(id => `:not(#id_${id})`).join("")
  textAreasSelector = `div > textarea${notSelector}`
  const textAreas = document.querySelectorAll(textAreasSelector)

  setTimeout(() => {
    textAreas.forEach(textArea => {
      new SimpleMDE({
        element: textArea,
        toolbar: [
          "bold", "italic", "heading", "|",
          "quote", "code", "link", "image", "|",
          "unordered-list", "ordered-list", "|",
          "undo", "redo", "|",
          "preview",
        ],
        spellChecker: false,
      })
    })
  }, 100)
})
