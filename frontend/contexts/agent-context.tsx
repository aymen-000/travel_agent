"use client"

import { createContext, useContext, useState, type ReactNode } from "react"

export type AgentType = "team" | "flights" | "hotels"

export interface Message {
  id: string
  content: string
  role: "user" | "assistant"
  timestamp: Date
  agentType: AgentType
}

interface AgentContextType {
  activeAgent: AgentType
  setActiveAgent: (agent: AgentType) => void
  messages: Record<AgentType, Message[]>
  addMessage: (agentType: AgentType, message: Omit<Message, "id" | "timestamp">) => void
  clearMessages: (agentType: AgentType) => void
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

const AgentContext = createContext<AgentContextType | undefined>(undefined)

export function AgentProvider({ children }: { children: ReactNode }) {
  const [activeAgent, setActiveAgent] = useState<AgentType>("team")
  const [messages, setMessages] = useState<Record<AgentType, Message[]>>({
    team: [],
    flights: [],
    hotels: [],
  })
  const [isLoading, setIsLoading] = useState(false)

  const addMessage = (agentType: AgentType, message: Omit<Message, "id" | "timestamp">) => {
    const newMessage: Message = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date(),
      agentType,
    }

    setMessages((prev) => ({
      ...prev,
      [agentType]: [...prev[agentType], newMessage],
    }))
  }

  const clearMessages = (agentType: AgentType) => {
    setMessages((prev) => ({
      ...prev,
      [agentType]: [],
    }))
  }

  return (
    <AgentContext.Provider
      value={{
        activeAgent,
        setActiveAgent,
        messages,
        addMessage,
        clearMessages,
        isLoading,
        setIsLoading,
      }}
    >
      {children}
    </AgentContext.Provider>
  )
}

export function useAgentContext() {
  const context = useContext(AgentContext)
  if (context === undefined) {
    throw new Error("useAgentContext must be used within an AgentProvider")
  }
  return context
}
