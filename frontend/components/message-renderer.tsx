"use client"

import { Card } from "@/components/ui/card"
import type { Message } from "@/contexts/agent-context"
import { User, Bot } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

interface MessageRendererProps {
  message: Message
}

export function MessageRenderer({ message }: MessageRendererProps) {
  const isUser = message.role === "user"

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3 px-2 md:px-0`}>
      <div
        className={`flex max-w-[85%] md:max-w-[80%] ${isUser ? "flex-row-reverse" : "flex-row"} items-start space-x-2`}
      >
        <div className={`flex-shrink-0 ${isUser ? "ml-2" : "mr-2"}`}>
          <div
            className={`w-7 h-7 md:w-8 md:h-8 rounded-full flex items-center justify-center ${
              isUser ? "bg-blue-500" : "bg-gray-500"
            }`}
          >
            {isUser ? (
              <User className="h-3 w-3 md:h-4 md:w-4 text-white" />
            ) : (
              <Bot className="h-3 w-3 md:h-4 md:w-4 text-white" />
            )}
          </div>
        </div>

        <Card
          className={`p-3 ${isUser ? "bg-blue-500 text-white" : "bg-white/90 backdrop-blur-sm border-0 shadow-lg"}`}
        >
          <div className="text-sm">
            {isUser ? (
              <p>{message.content}</p>
            ) : (
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                // className="prose prose-sm max-w-none"
                components={{
                  h1: ({ children }) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
                  h2: ({ children }) => <h2 className="text-base font-semibold mb-2">{children}</h2>,
                  h3: ({ children }) => <h3 className="text-sm font-semibold mb-1">{children}</h3>,
                  p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                  ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
                  ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
                  li: ({ children }) => <li className="text-sm">{children}</li>,
                  strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                  em: ({ children }) => <em className="italic">{children}</em>,
                  code: ({ children }) => (
                    <code className="bg-gray-100 px-1 py-0.5 rounded text-xs font-mono">{children}</code>
                  ),
                  pre: ({ children }) => (
                    <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto mb-2">{children}</pre>
                  ),
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-4 border-gray-300 pl-3 italic mb-2">{children}</blockquote>
                  ),
                  table: ({ children }) => (
                    <table className="border-collapse border border-gray-300 mb-2 text-xs">{children}</table>
                  ),
                  th: ({ children }) => (
                    <th className="border border-gray-300 px-2 py-1 bg-gray-100 font-semibold">{children}</th>
                  ),
                  td: ({ children }) => <td className="border border-gray-300 px-2 py-1">{children}</td>,
                }}
              >
                {message.content}
              </ReactMarkdown>
            )}
          </div>
          <div className={`text-xs mt-2 ${isUser ? "text-blue-100" : "text-gray-500"}`}>
            {message.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </div>
        </Card>
      </div>
    </div>
  )
}
