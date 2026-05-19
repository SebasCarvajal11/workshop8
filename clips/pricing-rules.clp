;;; Workshop 5 — Sistema experto de precios dinámicos (COOL + reglas)
;;; Clase Producto con 12 proposiciones del enunciado (slots en minúscula).

(defmodule MAIN
  (export ?ALL))

(defclass Producto
  (is-a USER)
  (slot codigo (type STRING))
  (slot da (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot db (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot ob (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot va (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot vb (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot ma (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot mb (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot tl (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot pf (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot eg (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot dr (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE))
  (slot ge (type SYMBOL) (allowed-values TRUE FALSE) (default FALSE)))

(deftemplate price-signal
  (slot kind (type SYMBOL) (allowed-values INCREASE DECREASE))
  (slot rule-id (type INTEGER))
  (slot reason (type STRING)))

(deftemplate discount-signal
  (slot kind (type SYMBOL) (allowed-values APPLY NO_DISCOUNT))
  (slot rule-id (type INTEGER))
  (slot reason (type STRING)))

(defrule rule-01-increase-high-demand-low-stock
  (object (is-a Producto) (da TRUE) (ob TRUE))
  =>
  (assert (price-signal (kind INCREASE) (rule-id 1)
           (reason "Demanda alta y existencias bajas")))
)

(defrule rule-02-discount-low-sales-high-margin
  (object (is-a Producto) (vb TRUE) (ma TRUE))
  =>
  (assert (discount-signal (kind APPLY) (rule-id 2)
           (reason "Ventas bajas con margen alto")))
)

(defrule rule-03a-discount-low-demand-margin-not-low
  (object (is-a Producto) (mb FALSE) (db TRUE))
  =>
  (assert (discount-signal (kind APPLY) (rule-id 3)
           (reason "Demanda baja y margen no es bajo")))
)

(defrule rule-03b-discount-low-sales-margin-not-low
  (object (is-a Producto) (mb FALSE) (vb TRUE))
  =>
  (assert (discount-signal (kind APPLY) (rule-id 3)
           (reason "Ventas bajas y margen no es bajo")))
)

(defrule rule-04-veto-discount-low-margin
  (declare (salience 100))
  (object (is-a Producto) (mb TRUE))
  =>
  (assert (discount-signal (kind NO_DISCOUNT) (rule-id 4)
           (reason "Margen bajo: no aplicar descuento")))
)

(defrule rule-05-increase-long-lead-high-demand
  (object (is-a Producto) (tl TRUE) (da TRUE))
  =>
  (assert (price-signal (kind INCREASE) (rule-id 5)
           (reason "Lead time largo con demanda alta")))
)

(defrule rule-06a-discount-warranty-low-sales
  (object (is-a Producto) (ge TRUE) (vb TRUE))
  =>
  (assert (discount-signal (kind APPLY) (rule-id 6)
           (reason "Garantía extendida con ventas bajas")))
)

(defrule rule-06b-discount-restricted-return
  (object (is-a Producto) (dr TRUE))
  =>
  (assert (discount-signal (kind APPLY) (rule-id 6)
           (reason "Devolución restringida")))
)

(defrule rule-07-increase-shipping-finance-margin-not-high
  (object (is-a Producto) (eg TRUE) (pf TRUE) (ma FALSE))
  =>
  (assert (price-signal (kind INCREASE) (rule-id 7)
           (reason "Envío gratis y financiamiento con margen no alto")))
)

(defrule rule-08-decrease-low-sales-stock-ok-lead-ok
  (object (is-a Producto) (vb TRUE) (ob FALSE) (tl FALSE))
  =>
  (assert (price-signal (kind DECREASE) (rule-id 8)
           (reason "Ventas bajas, inventario suficiente, lead time no largo")))
)

(defrule rule-09-discount-high-demand-low-sales-no-warranty
  (object (is-a Producto) (da TRUE) (va FALSE) (ge FALSE))
  =>
  (assert (discount-signal (kind APPLY) (rule-id 9)
           (reason "Demanda alta sin ventas altas ni garantía extendida")))
)

(defrule rule-10a-veto-discount-low-stock-high-demand
  (declare (salience 90))
  (object (is-a Producto) (ob TRUE) (da TRUE))
  =>
  (assert (discount-signal (kind NO_DISCOUNT) (rule-id 10)
           (reason "Stock bajo con demanda alta")))
)

(defrule rule-10b-veto-discount-low-stock-high-sales
  (declare (salience 90))
  (object (is-a Producto) (ob TRUE) (va TRUE))
  =>
  (assert (discount-signal (kind NO_DISCOUNT) (rule-id 10)
           (reason "Stock bajo con ventas altas")))
)

(defrule rule-11-decrease-restricted-return-no-warranty-low-sales
  (object (is-a Producto) (dr TRUE) (ge FALSE) (vb TRUE))
  =>
  (assert (price-signal (kind DECREASE) (rule-id 11)
           (reason "Devolución restringida, sin garantía, ventas bajas")))
)
