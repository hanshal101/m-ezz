import { createContext } from "react";

interface ContextType {
    isOpen: boolean;
    toggle_sidebar: () => void;
  }

export const context = createContext<ContextType | null>(null);