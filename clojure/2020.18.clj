(use '[io :rename {read-all-lines yummy, printI dbg}])
(use '[util :only (fargo)])
(use '[enum :only (slice)])

(defn tokens [expr]
  (loop [[acc [c & tail]] [[] expr]]
    (if (= \) c)
      [acc tail]
      (if (= \( c)
        (recur (apply (fargo #(conj acc %) identity) (tokens tail)))
        ;                               ^ this can be nil
        (if (empty? tail)
          (if (= nil c) acc (conj acc c))
          (recur [(conj acc c) tail])
          )))))

(defn evaluate [expr]
  (loop [[acc [op b & more]] [0 (concat [\+] expr)]]
    (as->
      (if (coll? b) (evaluate b) (Character/digit b 10)) x
      (case op
        \+ (+ acc x)
        \* (* acc x)
        )
      (if (empty? more)
        x
        (recur [x more])
        ))
    ))

(def inp
  (->> (yummy)
       (map (partial filter (partial not= \space)))
       (map tokens)
       ))

(->> inp
     (map evaluate)
     (reduce +)
     (println)
     )

; Part 2
; it should be as simple as evaluating addition in place, then evaluating multiplication
; NOTE: clojure doesn't hoist definitions so we can use the same name
(defn evaluate [expr]
  ; IRL we'd want to avoid doing this in the case we wanted to add more operators
  ; of course... we'd probably take an entirely different approach IRL.
  ; that is, it'd be worthwhile to implement a proper parser
  (reduce *
    (loop [[acc [op b & more]] [[0] (concat [\+] expr)]]
      (as->
        (if (coll? b) (evaluate b) (Character/digit b 10)) x
        (case op
          ; DONE: figure out why conj doesn't preserve order
          ; Answer: because, from the docs:
          ; "The 'addition' may happen at different 'places' depending on the concrete type."
          ; which means... I'm working with mixed types here?
          ; confirmed. they're parsed as Integer and cast to Long when I add them
          ;\+ (conj (slice acc 0 -1) (+ (last acc) x))
          ;\* (conj acc x)
          \+ (concat (slice acc 0 -1) [(+ (last acc) x)])
          \* (concat acc [x])
          )
        (if (empty? more)
          x
          (recur [x more])
          )))
    ))

(->> inp
     (map evaluate)
     (reduce +)
     (println)
     )

