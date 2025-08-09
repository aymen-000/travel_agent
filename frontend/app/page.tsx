"use client"

import { useState } from "react"
import { MobileSidebar } from "@/components/mobile-sidebar"
import { ChatInterface } from "@/components/chat-interface"
import { TravelSettings } from "@/components/travel-settings"
import { AgentProvider } from "@/contexts/agent-context"
import { TravelProvider } from "@/contexts/travel-context"

export default function Home() {
  const [activeView, setActiveView] = useState<"chat" | "settings">("chat")

  return (
    <TravelProvider>
      <AgentProvider>
        <div className="flex h-screen bg-gradient-to-br from-blue-400 via-purple-500 to-pink-500 relative overflow-hidden">
          <div className="absolute inset-0 bg-[url('/mountain-ocean-landscape.png')] bg-cover bg-center opacity-20"></div>
          <div className="absolute inset-0 bg-gradient-to-br from-blue-600/30 via-purple-600/30 to-pink-600/30"></div>

        
          <div className="absolute top-10 left-10 w-20 h-20 bg-white/10 rounded-full blur-xl animate-pulse"></div>
          <div className="absolute top-32 right-20 w-32 h-32 bg-white/5 rounded-full blur-2xl animate-pulse delay-1000"></div>
          <div className="absolute bottom-20 left-1/4 w-24 h-24 bg-white/10 rounded-full blur-xl animate-pulse delay-2000"></div>

          <MobileSidebar activeView={activeView} setActiveView={setActiveView} />
          <main className="flex-1 flex flex-col relative z-10">
            {activeView === "chat" ? <ChatInterface /> : <TravelSettings />}
          </main>
        </div>
      </AgentProvider>
    </TravelProvider>
  )
}
