import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { ChatFloating } from './chat/chat-floating'
import './index.css'
import reportWebVitals from './reportWebVitals'

if (process.env.NODE_ENV === 'development') {
  const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  )
}

const chatbotWrapper = document.createElement('div')
chatbotWrapper.setAttribute('id', 'chatbot')
chatbotWrapper.setAttribute('style', 'position: fixed; bottom: 0; right: 0; z-index: 9999;')
document.body.appendChild(chatbotWrapper)

const chatbotRoot =
  process.env.NODE_ENV === 'development'
    ? chatbotWrapper
    : chatbotWrapper.attachShadow({ mode: 'open' })
ReactDOM.createRoot(chatbotRoot).render(
  <React.StrictMode>
    <ChatFloating />
  </React.StrictMode>
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
