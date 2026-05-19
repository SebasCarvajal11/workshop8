;;; Ejecutar en CLIPS standalone:
;;; (load "pricing-rules.clp")
;;; (load "scenarios/ejemplo-alta-demanda.clp")
;;; (reset) (run) (facts)

(load "../pricing-rules.clp")

(defrule startup-scenario
  (declare (salience 10000))
  =>
  (make-instance escenario of Producto
    (codigo "ESC-01")
    (da TRUE)
    (db FALSE)
    (ob TRUE)
    (va FALSE)
    (vb TRUE)
    (ma TRUE)
    (mb FALSE)
    (tl FALSE)
    (pf FALSE)
    (eg FALSE)
    (dr FALSE)
    (ge FALSE))
)
