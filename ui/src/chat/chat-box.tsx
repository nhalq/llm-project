import { MinusIcon, PaperAirplaneIcon } from '@heroicons/react/24/outline'
import { useEffect, useRef, useState } from 'react'
import { Button } from '../components/button'
import { ChatBubble } from './chat-bubble'
import { Input } from 'components/input'

const ChatbotURL = process.env.CHATBOT_URL || 'https://lab.nhalq.dev/chatbot-api'

enum Identifier {
  Human = 'human',
  AI = 'ai',
}

interface Message {
  role: Identifier
  message: string | React.ReactElement
}

const initial: Message[] = [
  {
    role: Identifier.AI,
    message: 'Chào bạn, tôi có thể giúp gì cho bạn?',
  },
]

interface ChatBoxProps {
  conversationUUID: string
  open?: boolean
  onClose?: () => void
}

export function ChatBox({ conversationUUID, open = true, onClose }: ChatBoxProps) {
  const refMessageZone = useRef<HTMLDivElement>(null)
  const [messages, setMessages] = useState<Message[]>(initial)
  const [typings, setTypings] = useState<Message['role'][]>([])

  useEffect(() => {
    fetch(ChatbotURL + '/c/' + conversationUUID)
      .then((response) => response.json())
      .then(({ conversation }) => setMessages((messages) => messages.concat(conversation)))
      .catch(() => console.log('Không thể kết nối với chatbot'))
  }, [conversationUUID])

  useEffect(() => {
    const current = refMessageZone?.current
    current?.scrollTo({
      top: current.scrollHeight,
      behavior: 'smooth',
    })
  }, [refMessageZone, messages, typings])

  return (
    <div
      className="w-[384px] h-[512px] flex flex-col rounded-xl rounded-br-none bg-white shadow-xl transition-all duration-200 overflow-hidden [&>*]:px-4"
      style={open ? { opacity: 1 } : { width: 0, height: 0 }}
    >
      <div className="h-14 flex items-center shadow-sm">
        <div>
          <span className="font-bold">LLM chatbox</span>
          &nbsp;
          <span>(thanhnien.vn)</span>
        </div>
        <Button className="ml-auto p-0 border-0 size-10 rounded-full">
          <MinusIcon className="size-6" onClick={onClose} />
        </Button>
      </div>
      <div
        ref={refMessageZone}
        className="h-0 grow my-2 pt-2 pb-4 flex flex-col gap-4 overflow-auto rounded-xl"
      >
        {messages.map(({ role, message }, index) => (
          <ChatBubble key={index} role={role} message={message} />
        ))}
        {typings.map((role, index) => (
          <ChatBubble key={index} role={role} message={'Đang trả lời...'} />
        ))}
      </div>
      <form
        className="py-4 flex gap-2 border-t"
        onSubmit={(event: React.FormEvent<HTMLFormElement>) => {
          event.preventDefault()

          const messageTarget = event.currentTarget.message as HTMLInputElement | undefined
          if (!messageTarget?.value?.trim()) {
            return
          }

          const message = messageTarget.value.trim()
          setMessages((roles) => [...roles, { role: Identifier.Human, message }])
          setTypings((roles) => [...roles.filter((r) => r !== Identifier.AI), Identifier.AI])

          fetch(ChatbotURL + '/c/' + conversationUUID + '/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
          })
            .then((response) => response.json())
            .then(({ message }) => {
              setMessages((roles) => [...roles, { role: Identifier.AI, message }])
              setTypings((roles) => roles.filter((r) => r !== Identifier.AI))
            })

          messageTarget.value = ''
        }}
      >
        <Input name="message" placeholder="Gõ câu hỏi tại đây" autoComplete="off" />
        <Button type="submit" buttonType="primary">
          <PaperAirplaneIcon className="size-6" />
        </Button>
      </form>
    </div>
  )
}
