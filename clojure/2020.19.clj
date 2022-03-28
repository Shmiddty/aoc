(use '[io :rename {read-all yummy, printI dbg}])
(use '[clojure.string :only (split)])
(use '[util :only (fargo)])
(use '[enum :only (make-hash-map, cross)])

(def inp
  (->> (yummy)
       (#(split % #"\n\n"))
       (apply
         (fargo
           (fn [rules]
             (->> (split rules #"\n")
                  (map (partial re-matches #"(\d+): (\"(([ab]))\"|((\d+ ?)+)\|? ?((\d+ ?)*))"))
                  (map rest)
                  (map (partial take-nth 2))
                  (map (partial filter identity))
                  (map (juxt first (fn [toks] (filter not-empty (map #(filter not-empty (split % #" ")) (rest toks))))))
                  ; I need to come up with a better way of parsing inputs
                  (make-hash-map)
                  ))
           #(split % #"\n")
           ))
       ))

(def rules (first inp))
(def make
  (memoize
    (fn [rule]
      (if (contains? rules rule)
        (mapcat
          (fn [subrule]
            (reduce
              (fn [acc v] (map (partial apply str) (cross acc v)))
              [""]
              (map make subrule)
              ))
          (get rules rule)
          )
        [rule]
        ))))

(def validzero (set (make "0")))
(def messages (second inp))

(->> messages
     (filter (partial contains? validzero))
     (count)
     (println)
     )

; brain is drained. save part 2 for later.
; 0: 8 11
; 8: 42 | 42 8
; 11: 42 31 | 42 11 31
; X 42s then Y 42s then Y 31s
; so... going from the right, count the number of 31s
; the rest of the partitions must be 42s
; and there must more 42s than 31s
; (going from the right was an unnecessary step, so I didn't do that in the end)
(def fortytwo (set (make "42")))
(def partsize (count (first fortytwo)))
(def thirtyone (set (make "31")))

(defn validate [message]
  (->> message
       (partition-all partsize)
       (map (partial apply str))
       (partition-by (partial contains? fortytwo))
       ((juxt first second))
       (apply (fargo count #(count (filter (partial contains? thirtyone) %))))
       (apply
         #(and
            (> %2 0)
            (> %1 %2)
            (= (* (+ %1 %2) partsize) (count message))
            ))
       ))

(->> messages
     (filter validate)
     (count)
     (println)
     )

; 257 too high
; 260 definitely too high
; 253 may be correct
