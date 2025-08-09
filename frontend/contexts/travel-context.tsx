"use client"

import { createContext, useContext, useState, type ReactNode } from "react"

export interface TravelPreferences {
  departureDate: string
  endDate: string
  destination: string
  numGuests: number
}

interface TravelContextType {
  preferences: TravelPreferences
  updatePreferences: (updates: Partial<TravelPreferences>) => void
  resetPreferences: () => void
}

const defaultPreferences: TravelPreferences = {
  departureDate: "",
  endDate: "",
  destination: "",
  numGuests: 2,
}

const TravelContext = createContext<TravelContextType | undefined>(undefined)

export function TravelProvider({ children }: { children: ReactNode }) {
  const [preferences, setPreferences] = useState<TravelPreferences>(defaultPreferences)

  const updatePreferences = (updates: Partial<TravelPreferences>) => {
    setPreferences((prev) => ({ ...prev, ...updates }))
  }

  const resetPreferences = () => {
    setPreferences(defaultPreferences)
  }

  return (
    <TravelContext.Provider value={{ preferences, updatePreferences, resetPreferences }}>
      {children}
    </TravelContext.Provider>
  )
}

export function useTravelContext() {
  const context = useContext(TravelContext)
  if (context === undefined) {
    throw new Error("useTravelContext must be used within a TravelProvider")
  }
  return context
}
