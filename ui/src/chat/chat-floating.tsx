import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline'
import { ChatBox } from 'chat/chat-box'
import { useState } from 'react'
import { v4 as uuidv4 } from 'uuid'

function getOrCreateChatbotPayload() {
  const k = '@nhalq/llm-chatbox'
  const payload = window.localStorage.getItem(k)
  if (payload) {
    const { expiry } = JSON.parse(payload)
    if (new Date(expiry) > new Date()) {
      return JSON.parse(payload)
    }
  }

  const uuid = uuidv4()
  const MilisecondsInHour = 60 * 60 * 1000
  const expiry = new Date(Date.now() + 8 * MilisecondsInHour).toISOString()

  const v = { uuid, expiry }
  window.localStorage.setItem(k, JSON.stringify(v))
  return v
}

export function ChatFloating() {
  const { uuid } = getOrCreateChatbotPayload()
  const [open, setOpen] = useState(process.env.NODE_ENV === 'development')

  return (
    <div className="fixed bottom-8 right-8">
      <button className="relative" onClick={() => setOpen(true)}>
        <div
          className="relative size-12 flex items-center justify-center rounded-full border bg-white"
          onClick={() => setOpen(true)}
        >
          <ChatBubbleLeftRightIcon className="size-6" />
        </div>
      </button>
      <div className="absolute bottom-0 right-0 transition-all">
        <ChatBox conversationUUID={uuid} open={open} onClose={() => setOpen(false)} />
      </div>
    </div>
  )
}
