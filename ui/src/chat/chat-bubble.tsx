import clsx from 'clsx'
import React from 'react'
import Markdown from 'react-markdown'

interface ChatBubbleProps {
  message: string | React.ReactElement
  role: 'human' | 'ai'
}

const BubbleCommonClass = 'px-4 py-2 max-w-52 flex items-center rounded-md'

function BubbleAvatar({ children }: React.PropsWithChildren<{}>) {
  return (
    <div className="flex items-center justify-center size-10 rounded-full text-2xl">{children}</div>
  )
}

function LeftBubble({ children }: React.PropsWithChildren) {
  return (
    <div className="mr-auto flex items-end gap-2">
      <BubbleAvatar>🤖</BubbleAvatar>
      <div className={clsx(BubbleCommonClass, 'bg-slate-50')}>{children}</div>
    </div>
  )
}

function RightBubble({ children }: React.PropsWithChildren) {
  return (
    <div className="ml-auto flex items-end gap-2">
      <div className={clsx(BubbleCommonClass, 'bg-amber-200')}>{children}</div>
      <BubbleAvatar>🦦</BubbleAvatar>
    </div>
  )
}

type ChatContentProps = {
  content: string | React.ReactElement
}

function ChatContent({ content }: ChatContentProps) {
  if (typeof content === 'string') {
    return (
      <article className="prose prose-slate [&_*]:my-0">
        <Markdown children={content} />
      </article>
    )
  }

  return content
}

export function ChatBubble({ role, message }: ChatBubbleProps) {
  const content = <ChatContent content={message} />
  switch (role) {
    case 'human':
      return <RightBubble>{content}</RightBubble>
    case 'ai':
      return <LeftBubble>{content}</LeftBubble>
    default:
      return content
  }
}
