"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { useAgentContext, type AgentType } from "@/contexts/agent-context"
import { useTravelContext } from "@/contexts/travel-context"
import { Plane, Hotel, Users, Settings, MessageCircle, MapPin, Menu } from "lucide-react"

interface MobileSidebarProps {
  activeView: "chat" | "settings"
  setActiveView: (view: "chat" | "settings") => void
}

const agentConfig = {
  team: {
    name: "Travel Team",
    icon: Users,
    description: "General travel planning",
    color: "bg-blue-500",
  },
  flights: {
    name: "Flight Expert",
    icon: Plane,
    description: "Flight bookings",
    color: "bg-green-500",
  },
  hotels: {
    name: "Hotel Specialist",
    icon: Hotel,
    description: "Hotel bookings",
    color: "bg-purple-500",
  },
}

export function MobileSidebar({ activeView, setActiveView }: MobileSidebarProps) {
  const [isOpen, setIsOpen] = useState(false)
  const { activeAgent, setActiveAgent, messages, clearMessages } = useAgentContext()
  const { preferences } = useTravelContext()

  const handleAgentSwitch = (agent: AgentType) => {
    setActiveAgent(agent)
    setActiveView("chat")
    setIsOpen(false)
  }

  const SidebarContent = () => (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-900 flex items-center gap-2">
          <MapPin className="h-5 w-5 text-blue-500" />
          TravelAI
        </h1>
        <p className="text-xs text-gray-600 mt-1">Your AI Travel Assistant</p>
      </div>

      {/* Travel Summary */}
      {preferences.destination && (
        <div className="p-3 border-b border-gray-200">
          <Card className="p-3 bg-blue-50/80 backdrop-blur-sm">
            <h3 className="font-semibold text-sm text-blue-900">Current Trip</h3>
            <p className="text-sm text-blue-700 truncate">{preferences.destination}</p>
            <div className="flex justify-between text-xs text-blue-600 mt-1">
              <span>
                {preferences.departureDate ? new Date(preferences.departureDate).toLocaleDateString() : "No date"}
              </span>
              <span>{preferences.numGuests} guests</span>
            </div>
          </Card>
        </div>
      )}

      {/* Navigation */}
      <div className="p-3 border-b border-gray-200">
        <div className="space-y-2">
          <Button
            variant={activeView === "chat" ? "default" : "ghost"}
            className="w-full justify-start text-sm"
            onClick={() => {
              setActiveView("chat")
              setIsOpen(false)
            }}
          >
            <MessageCircle className="h-4 w-4 mr-2" />
            Chat
          </Button>
          <Button
            variant={activeView === "settings" ? "default" : "ghost"}
            className="w-full justify-start text-sm"
            onClick={() => {
              setActiveView("settings")
              setIsOpen(false)
            }}
          >
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </Button>
        </div>
      </div>

      {/* Agents */}
      <div className="flex-1 p-3">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">AI Agents</h3>
        <div className="space-y-2">
          {Object.entries(agentConfig).map(([key, config]) => {
            const agentKey = key as AgentType
            const Icon = config.icon
            const messageCount = messages[agentKey].length

            return (
              <div key={key} className="relative">
                <Button
                  variant={activeAgent === agentKey ? "default" : "ghost"}
                  className="w-full justify-start p-3 h-auto text-sm"
                  onClick={() => handleAgentSwitch(agentKey)}
                >
                  <div className={`p-1.5 rounded-lg ${config.color} mr-3`}>
                    <Icon className="h-3 w-3 text-white" />
                  </div>
                  <div className="text-left flex-1">
                    <div className="font-medium text-sm">{config.name}</div>
                    <div className="text-xs text-gray-500 truncate">{config.description}</div>
                  </div>
                  {messageCount > 0 && (
                    <span className="bg-blue-500 text-white text-xs rounded-full px-2 py-1 ml-2">{messageCount}</span>
                  )}
                </Button>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )

  return (
    <>
      <div className="md:hidden fixed top-4 left-4 z-50">
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
          <SheetTrigger asChild>
            <Button variant="outline" size="sm" className="bg-white/90 backdrop-blur-sm">
              <Menu className="h-4 w-4" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-80 p-0">
            <SidebarContent />
          </SheetContent>
        </Sheet>
      </div>

      <div className="hidden md:flex w-80 bg-white/95 backdrop-blur-sm border-r border-gray-200 flex-col">
        <SidebarContent />
      </div>
    </>
  )
}
