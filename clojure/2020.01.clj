; (slurp *in*) - all input as a single string
; read/read-line - the next line in the input
; (line-seq (java.io.BufferedReader. *in*)) - all lines in an... array? vector? tuple?
; (take-while identity (repeatedly #(.readLine *in*))) - same as above

;(ns one
;  (:require [io]))
;(use '[io :only [read-all]])
;(use 'io)
(use '[io :rename {read-all-lines yummy}])
(use '[enum])

(def inp (->> (yummy) (map read-string)))

(->> inp
     (pairs)
     (filter #(= (reduce + %) 2020))
     (first)
     (reduce *)
     (println))

(->> inp
     (combinations 3)
     (filter #(= (reduce + %) 2020))
     (first)
     (reduce *)
     (println))

