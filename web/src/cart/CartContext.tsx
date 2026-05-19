import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import type { CartLine } from "../types";

interface CartContextValue {
  items: CartLine[];
  count: number;
  addItem: (line: Omit<CartLine, "quantity"> & { quantity?: number }) => void;
  updateQty: (sku: string, quantity: number) => void;
  removeItem: (sku: string) => void;
  setFinancing: (sku: string, value: boolean) => void;
  clear: () => void;
}

const CartContext = createContext<CartContextValue | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartLine[]>([]);

  const addItem = useCallback(
    (line: Omit<CartLine, "quantity"> & { quantity?: number }) => {
      setItems((prev) => {
        const existing = prev.find((i) => i.sku === line.sku);
        if (existing) {
          return prev.map((i) =>
            i.sku === line.sku
              ? { ...i, quantity: i.quantity + (line.quantity ?? 1) }
              : i,
          );
        }
        return [
          ...prev,
          {
            sku: line.sku,
            name: line.name,
            quantity: line.quantity ?? 1,
            financing_requested: line.financing_requested ?? false,
          },
        ];
      });
    },
    [],
  );

  const updateQty = useCallback((sku: string, quantity: number) => {
    setItems((prev) =>
      prev
        .map((i) => (i.sku === sku ? { ...i, quantity } : i))
        .filter((i) => i.quantity > 0),
    );
  }, []);

  const removeItem = useCallback((sku: string) => {
    setItems((prev) => prev.filter((i) => i.sku !== sku));
  }, []);

  const setFinancing = useCallback((sku: string, value: boolean) => {
    setItems((prev) =>
      prev.map((i) =>
        i.sku === sku ? { ...i, financing_requested: value } : i,
      ),
    );
  }, []);

  const clear = useCallback(() => setItems([]), []);

  const count = useMemo(
    () => items.reduce((acc, i) => acc + i.quantity, 0),
    [items],
  );

  const value = useMemo(
    () => ({
      items,
      count,
      addItem,
      updateQty,
      removeItem,
      setFinancing,
      clear,
    }),
    [items, count, addItem, updateQty, removeItem, setFinancing, clear],
  );

  return (
    <CartContext.Provider value={value}>{children}</CartContext.Provider>
  );
}

export function useCart(): CartContextValue {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart debe usarse dentro de CartProvider");
  return ctx;
}
