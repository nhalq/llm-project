import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import App from './App'
import reportWebVitals from './reportWebVitals'
import { ChatFloating } from './chat/chat-floating'

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)

const e = document.createElement('div')
ReactDOM.createRoot(e).render(
  <React.StrictMode>
    <ChatFloating />
  </React.StrictMode>
)

window.addEventListener('load', () => {
  document.body.appendChild(e)
})

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
