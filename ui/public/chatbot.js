;(function LLMChatBot() {
  const ScriptURL = ''
  const StyleSheetURL = ''

  function injectReactScript(parent) {
    const script = document.createElement('script')
    script.setAttribute('src', ScriptURL)
    parent.appendChild(script)
  }

  function injectStyleSheet(parent) {
    const stylesheet = document.createElement('link')
    stylesheet.setAttribute('rel', 'stylesheet')
    stylesheet.setAttribute('href', StyleSheetURL)
    parent.appendChild(stylesheet)
  }

  async function observe(selector) {
    return new Promise((resolve, reject) => {
      const id = setTimeout(() => reject(new Error('Can not insert chatbot (timeout)')), 5000)
      const observer = new MutationObserver(() => {
        const elements = selector()
        if (elements) {
          clearTimeout(id)
          observer.disconnect()
          resolve(elements)
        }
      })

      observer.observe(document.body, {
        childList: true,
        subtree: true,
      })
    })
  }

  injectReactScript(document.head)
  observe(() => document.getElementById('chatbot'))
    .then((shadowWrapper) => injectStyleSheet(shadowWrapper.shadowRoot))
    .catch((error) => alert(error.message))
})()
